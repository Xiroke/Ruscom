// Функция для получения данных узлов (node) графа из HTML
function getNodeDataFromHTML() {
  return Array.from(document.querySelectorAll("#node-data > div")).map(
    (div) => ({
      id: div.getAttribute("data-id"),
      label: div.getAttribute("data-label"),
      guidebook_item_title: div.getAttribute("data-pack_guidebook_item_title").split("[").join('').split("]").join('').split("'").join('').split(', '),
      guidebook_item_id: div.getAttribute("data-pack_guidebook_item_id").split("[").join('').split("]").join('').split(', '),
      guidebook_item_type: div.getAttribute("data-pack_guidebook_item_type").split("[").join('').split("]").join('').split(">").join('').split('<').join('').split(', '),
      angle: Math.random() * 2 * Math.PI,
      radius: (Math.random() + 0.4) * 300,
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
  .attr("preserveAspectRatio", "xMidYMid meet")
  .call(d3.zoom().on("zoom", zoomed));

const container = svg.append("g");

// Функция для масштабирования и перетаскивания
function zoomed(event) {
  container.attr("transform", event.transform);
}

// Создание симуляции силового графа
const simulation = d3
  .forceSimulation(graphData.nodes)
  .force(
    "link",
    d3.forceLink(graphData.links).id((d) => d.id).distance(100)
  )
  .force("charge", d3.forceManyBody().strength(-1000))
  .force("center", d3.forceCenter(window.innerWidth / 2, window.innerHeight / 2))
  .alphaDecay(0.02)
  .on("tick", ticked);

// Отрисовка связей (links) на SVG элементе
const link = container
  .append("g")
  .attr("stroke", "#999")
  .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(graphData.links)
  .join("line");

// Отрисовка узлов (nodes) на SVG элементе
const node = container
  .append("g")
  .selectAll("circle")
  .data(graphData.nodes)
  .join("circle")
  .attr("r", (d) => (d.label === "Ruscom" ? 30 : 20))
  .attr("fill", "#515266")
  .on("click", (event, d) => showNodeTooltip(event, d))
  .call(
    d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
  );

// Скрытие всплывающего окна при клике вне узла
document.addEventListener("click", (event) => {
  const tooltip = document.querySelector(".tooltip");
  if (tooltip.style.display !== "none" && !event.target.closest(".tooltip")) {
    hideNodeTooltip(event);
  }
});

// Добавление текста с названием узла рядом с каждым узлом
const text = container
  .append("g")
  .selectAll("text")
  .data(graphData.nodes)
  .join("text")
  .text((d) => d.label)
  .attr("text-anchor", "middle")
  .attr("class", "node-text");

// Добавление всплывающих подсказок к узлам
node.append("title").text((d) => d.label);

// Переменные для вращения узлов вокруг центра
const rotationSpeed = 0.002;

// Функция для обновления позиций узлов и связей в графе
function ticked() {
  link
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);

  node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

  text.attr("x", (d) => d.x).attr("y", (d) => d.y + 40);
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

function createObjectOfPack(parent, pack_title, pack_id, pack_type) {
  let theories = document.createElement('div');
  let tasks = document.createElement('div');
  theories.className = 'tooltip_theories';
  theories.innerHTML = 'Теория';
  tasks.innerHTML = 'Задание';
  tasks.className = 'tooltip_tasks';
  for (let i = 0; i < pack_title.length; i++) {
    if (pack_title[i] != "") {
      
      let task = document.createElement('div');
      let url = document.createElement('a');
      url.href = '../task_item/' + pack_id[i];
      task.innerHTML = pack_title[i];
      task.classList.add('tooltip_task');
      url.classList.add('tooltip_task_url');
      url.appendChild(task);
      console.log(pack_type[i])
      switch (pack_type[i]) {
        case 'Theory':
          theories.appendChild(url);
          break;
        case 'TaskSimple':
          tasks.appendChild(url);
          break;

        case 'TaskDifficultАrchitecture':
          tasks.appendChild(url);
          break;
      }
      parent.appendChild(theories);
      parent.appendChild(tasks);
    } else {
      console.log('')
    }
  }
}

function showNodeTooltip(event, d) {
  event.stopPropagation();
  const tooltip = document.querySelector(".tooltip");
  const tooltipLabel = document.querySelector(".tooltip_label");
  const overlay = document.querySelector(".overlay");

  let tooltip_item = document.createElement('div');
  tooltip_item.className = 'tooltip_item';
  tooltip.appendChild(tooltip_item);
  createObjectOfPack(tooltip_item, d.guidebook_item_title, d.guidebook_item_id, d.guidebook_item_type);

  tooltipLabel.innerHTML = d.label;

  tooltip.style.display = "block";
  overlay.style.display = "block";
}

function hideNodeTooltip(event) {
  const tooltip = document.querySelector(".tooltip");
  const tooltip_item = document.querySelector(".tooltip_item");
  const overlay = document.querySelector(".overlay");

  tooltip_item.parentNode.removeChild(tooltip_item);
  tooltip.style.display = "none";
  overlay.style.display = "none";
}
