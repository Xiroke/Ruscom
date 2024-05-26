document.addEventListener('DOMContentLoaded', function () {
  const items = document.querySelectorAll('.frequent-question_item_question');

  items.forEach(item => {
      item.addEventListener('click', function () {
          const answer = this.nextElementSibling;
          const arrow = this.querySelector('.arrow');

          if (answer.classList.contains('open')) {
              answer.classList.remove('open');
              arrow.style.transform = 'rotate(0deg)';
          } else {
              answer.classList.add('open');
              arrow.style.transform = 'rotate(180deg)';
          }
      });
  });
});
