const xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
const yValues = [55, 49, 44, 24, 15];

new Chart("history-chart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      data: yValues
    }]
  },
  options: {}
}); 
