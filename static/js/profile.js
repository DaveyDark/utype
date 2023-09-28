const xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
const yValues = [55, 49, 44, 24, 15];
Chart.defaults.global.defaultFontColor = "#fff";

const user_id = document.getElementById('user-id').value

fetch(`/api/graphs/${user_id}`).then(res => {
    return res.json()
  }).then(stats => {
    var data = {
      labels: stats.map(x => x.timestamp),
      datasets: [
        {
          label: 'Score',
          data: stats.map(x => x.score),
          borderColor: '#eb75a4',
          borderWidth: 2
        },
        {
          label: 'WPM',
          data: stats.map(x => x.wpm),
          borderColor: '#e55d73',
          borderWidth: 2
        },
        {
          label: 'Accuracy',
          data: stats.map(x => x.accuracy),
          borderColor: '#5cb4c4',
          borderWidth: 2
        }
      ]
    };

    // Define the configuration options for the chart
    var options = {
      scales: {
        y: {
          beginAtZero: true,
        }
      },
    };

    new Chart("history-chart", {
      type: "line",
      data: data,
      options: options,
    }); 
  }).catch(err => {
    console.error(`Error: ${err}`)
  })

