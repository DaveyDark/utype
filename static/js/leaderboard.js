Chart.defaults.global.defaultFontColor = "#fff";

fetch(`/api/scores-graph`).then(res => {
    return res.json()
  }).then(stats => {
    var data = {
      labels: stats.map(x => x.username),
      datasets: [
        {
          label: 'Score',
          data: stats.map(x => x.score),
          borderColor: '#eb75a4',
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

    new Chart("leaderboard-chart", {
      type: "bar",
      data: data,
      options: options,
    }); 
  }).catch(err => {
    console.error(`Error: ${err}`)
  })

