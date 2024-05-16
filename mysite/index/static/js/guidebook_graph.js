// Функция для получения данных узлов графа из HTML
function getNodeDataFromHTML() {
  return Array.from(document.querySelectorAll("#node-data > div")).map(
    (div) => ({
      id: div.getAttribute("data-id"),
      label: div.getAttribute("data-label"),
      pack_tasks_title: div.getAttribute("data-pack_tasks_title").split("[").join('').split("]").join('').split("'").join('').split(','),
      pack_tasks_id: div.getAttribute("data-pack_tasks_id").split("[").join('').split("]").join('').split(', '),
    })
  );
}

// Функция для получения данных связей (link) графа из HTML
function getLinkDataFromHTML() {
  return Array.from(document.querySelectorAll("#link-data > div")).map(
    (div) => ({
      source: div.getAttribute("data-source"),
      target: div.getAttribute("data-target"),
    })
  );
}

// Получаем данные узлов и связей графа из HTML
const graphData = {
  nodes: getNodeDataFromHTML(),
  links: getLinkDataFromHTML(),
};

// Создание SVG элемента для отображения графа
const svg = d3
  .select("#graph-container")
  .append("svg")
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("viewBox", [0, 0, 1920, 1080])
  .attr("preserveAspectRatio", "xMidYMid meet");

// Создание симуляции силового графа
const simulation = d3
  .forceSimulation(graphData.nodes)
  .force(
    "link",
    d3.forceLink(graphData.links).id((d) => d.id)
  )
  .force("charge", d3.forceManyBody().strength(-1000)) // Отталкивание между узлами
  .force("center", d3.forceCenter(window.innerWidth/2, window.innerHeight/2))
  .force("node-text", d3.forceManyBody().strength(-2000))
  .on("tick", ticked);

  
// Отрисовка связей (links) на SVG элементе
const link = svg
  .append("g")
  .attr("stroke", "#999")
  .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(graphData.links)
  .join("line");

// Отрисовка узлов (nodes) на SVG элементе
const node = svg
  .append("g")
  .selectAll("circle")
  .data(graphData.nodes)
  .join("circle")
  .attr("r", 13)
  .attr("fill", "#9f9f9f")
  .on("click", (event, d) => showNodeTooltip(event, d)) // Показываем всплывающее окно при клике
  .call(
    d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended)
  );

// Скрытие всплывающего окна при клике вне узла
document.addEventListener("click", (event) => {
  const tooltip = document.querySelector(".tooltip");
  if (!tooltip.style.display == "none") {
    hideNodeTooltip(event);
  }
});

// Добавление текста с названием узла рядом с каждым узлом
const text = svg
  .append("g")
  .selectAll("text")
  .data(graphData.nodes)
  .join("text")
  .attr("x", 8)
  .attr("y", 4)
  .text((d) => d.label);

// Добавление всплывающих подсказок к узлам
node.append("title").text((d) => d.label);

// Функция для обновления позиций узлов и связей в графе
function ticked() {
  link
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);

  node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

  text.attr("x", (d) => d.x).attr("y", (d) => d.y + 30);
  text.attr("text-anchor", "middle");
  text.attr("class", "node-text");
}

// Функции для перетаскивания узлов
function dragstarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragended(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function showNodeTooltip(event, d) {
  const tooltip = document.querySelector(".tooltip");
  const tooltipLabel = document.querySelector(".tooltip_label");
  const overlay = document.querySelector(".overlay");

  const pack_tasks_title = d.pack_tasks_title;
  let tooltip_tasks = document.createElement('div');
  tooltip_tasks.id = 'tooltip_tasks';
  tooltip.appendChild(tooltip_tasks);
  console.log(typeof(pack_tasks_title));
  console.log(d.tasks_id);
  for(let i = 0; i < pack_tasks_title.length; i++) {
    if (pack_tasks_title != ""){
      task = document.createElement('div');
      url = document.createElement('a');
      url.href = '../task_type1/' + d.pack_tasks_id[i];
      url.innerHTML = pack_tasks_title[i];
      task.appendChild(url);
      task.classList.add('tooltip_task');
      tooltip_tasks.appendChild(task);
    }
    else {
      console.log('')
    };
  };

  // Устанавливаем текст всплывающего окна
  tooltipLabel.innerHTML = d.label;
  


  // Показываем всплывающее окно
  tooltip.style.display = "block";
  // Показываем затемнение фона
  overlay.style.display = "block";
}

function hideNodeTooltip(event) {
  const tooltip = document.querySelector(".tooltip");
  const overlay = document.querySelector(".overlay");

  tooltip.removeChild(document.getElementById('tooltip_tasks'));
  // Скрываем всплывающее окно и затемнение фона
  tooltip.style.display = "none";
  overlay.style.display = "none";
}
