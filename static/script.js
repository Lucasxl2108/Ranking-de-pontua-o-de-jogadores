// static/script.js
document.addEventListener('DOMContentLoaded', function() {
    const listaSelect = document.getElementById('lista-select');
    const rankingBody = document.querySelector('#ranking-table tbody');

    // Função para buscar e exibir um ranking específico
    async function fetchRanking(listaId) {
        rankingBody.innerHTML = '<tr><td colspan="5">Carregando...</td></tr>'; // Alterado colspan para 5
        try {
            const response = await fetch(`/api/ranking/${listaId}`);
            const rankingData = await response.json();

            rankingBody.innerHTML = ''; // Limpa a tabela

            if (rankingData.length === 0) {
                rankingBody.innerHTML = '<tr><td colspan="5">Nenhum jogador nesta lista.</td></tr>'; // Alterado colspan para 5
                return;
            }
            
            const topClasses = ['top-1', 'top-2', 'top-3'];

            rankingData.forEach((player, index) => {
                const row = document.createElement('tr');
                const rank = index + 1;

                if (rank <= 3) {
                    row.classList.add(topClasses[index]);
                }

                // Lógica para o ícone de 'previous' (exemplo simples)
                let previousIcon = '<i class="fas fa-minus previous-icon"></i>'; // Default
                if (player.pontuacao > 1000) {
                    previousIcon = '<i class="fas fa-arrow-up previous-icon"></i>';
                } else if (player.pontuacao < 1000) {
                    previousIcon = '<i class="fas fa-arrow-down previous-icon"></i>';
                }

                row.innerHTML = `
                    <td>${rank}</td>
                    <td class="name-col">${player.nome}</td>
                    <td>${player.nivel}</td>
                    <td>${player.pontuacao.toFixed(2)}</td>
                    <td>${previousIcon}</td>
                `;
                rankingBody.appendChild(row);
            });

        } catch (error) {
            console.error('Erro ao buscar ranking:', error);
            rankingBody.innerHTML = '<tr><td colspan="5">Erro ao carregar ranking.</td></tr>'; // Alterado colspan para 5
        }
    }

    // Função para carregar a lista de rankings disponíveis
    async function loadListas() {
        try {
            const response = await fetch('/api/listas');
            const listas = await response.json();

            listaSelect.innerHTML = ''; // Limpa as opções

            if (listas.length > 0) {
                listas.forEach(lista => {
                    const option = document.createElement('option');
                    option.value = lista.id;
                    option.textContent = `${lista.timestamp} (ID: ${lista.id})`;
                    listaSelect.appendChild(option);
                });
                // Exibe o primeiro ranking da lista por padrão
                fetchRanking(listas[0].id);
            } else {
                const option = document.createElement('option');
                option.textContent = 'Nenhuma lista carregada';
                listaSelect.appendChild(option);
                rankingBody.innerHTML = '';
            }
        } catch (error) {
            console.error('Erro ao buscar listas:', error);
        }
    }

    // Evento para quando uma nova lista é selecionada
    listaSelect.addEventListener('change', (event) => {
        const selectedId = event.target.value;
        if (selectedId) {
            fetchRanking(selectedId);
        }
    });

    // Carrega as listas iniciais quando a página é aberta
    loadListas();
});