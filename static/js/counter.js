
const counters = document.querySelectorAll('.counter');
const speed = 150;

counters.forEach(counter => {
  const targetValue = Number(counter.getAttribute('val'))
  const initial = counter.textContent;
  const increment = targetValue / (speed / 1000);
  let currentValue = 0;
  
  const interval = setInterval(() => {
    if (currentValue >= targetValue) {
      counter.textContent = targetValue + initial;
      clearInterval(interval);
    } else {
      currentValue += increment/1000;
      counter.textContent = currentValue.toFixed(1) + initial;
    }
  }, 1);
});
