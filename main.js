const CLOCK_CATEGORIES = ["Sleep", "Work/Education", "Household/Care", "Leisure", "Travel"];
const CATEGORY_ORDER = ["Sleep", "Work/Education", "Household/Care", "Leisure", "Social", "Travel", "Other"];
const AGES = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"];

const CATEGORY = {
  Sleep: {
    color: "#5267a8",
    rooms: ["Sleep"],
    description: "The time your body asks for"
  },
  "Work/Education": {
    color: "#bf5b4b",
    rooms: ["Work", "Education"],
    description: "Hours that belong to institutions"
  },
  "Household/Care": {
    color: "#8f7a58",
    rooms: ["Household Activities", "Caregiving"],
    description: "The work no one pays you for"
  },
  Leisure: {
    color: "#4f9f7a",
    rooms: ["Leisure"],
    description: "The part of the day that still feels like yours"
  },
  Social: {
    color: "#7e6ab2",
    rooms: [],
    description: "The hours spent with other people"
  },
  Travel: {
    color: "#d68145",
    rooms: ["Travel"],
    description: "The time between places"
  },
  Other: {
    color: "#9c9a91",
    rooms: [],
    description: "Everything not separated in the processed data"
  }
};

const RAW_TO_CATEGORY = {
  Sleep: "Sleep",
  Work: "Work/Education",
  Education: "Work/Education",
  "Household Activities": "Household/Care",
  Caregiving: "Household/Care",
  Leisure: "Leisure",
  Travel: "Travel"
};

const STAGE_COPY = {
  "18-24": {
    title: "Age 18-24",
    sentence: "Time still feels open. School, leisure, friends, sleep, and screens compete for space.",
    summary: "Her day is still loose around the edges."
  },
  "25-34": {
    title: "Age 25-34",
    sentence: "Work enters the center of the day, and flexible hours begin to gather around obligations.",
    summary: "Her day starts answering to work."
  },
  "35-44": {
    title: "Age 35-44",
    sentence: "Paid work is joined by unpaid work: chores, errands, and care.",
    summary: "Her day is crowded with visible and invisible work."
  },
  "45-54": {
    title: "Age 45-54",
    sentence: "Work remains large, but personal time becomes more fragmented.",
    summary: "Her day is compressed into routines."
  },
  "55-64": {
    title: "Age 55-64",
    sentence: "Some time loosens, but not evenly; work and care still shape the day.",
    summary: "Her day starts to open, with conditions."
  },
  "65+": {
    title: "Age 65+",
    sentence: "Time returns, but differently: routine, health, and social life shape the open space.",
    summary: "Her day has more room, but that room has a texture."
  }
};

const TRADEOFFS = {
  "work-leisure": {
    title: "Work vs leisure",
    subtitle: "Institutional time rises through midlife while leisure contracts, then returns later.",
    series: [
      { label: "Work/Education", category: "Work/Education", value: age => categoryHours(age, "Work/Education") },
      { label: "Leisure", category: "Leisure", value: age => categoryHours(age, "Leisure") }
    ]
  },
  "care-personal": {
    title: "Care vs personal time",
    subtitle: "Unpaid work grows in the crowded middle of life while personal time competes for room.",
    series: [
      { label: "Household/Care", category: "Household/Care", value: age => categoryHours(age, "Household/Care") },
      { label: "Leisure", category: "Leisure", value: age => categoryHours(age, "Leisure") }
    ]
  },
  "alone-social": {
    title: "Alone vs social time",
    subtitle: "Social context is measured separately from activities, so these hours can overlap the activity categories.",
    series: [
      { label: "Alone", category: "Other", value: age => socialHours(age, "Alone") },
      { label: "Social", category: "Social", value: age => socialHours(age, "Together") }
    ]
  },
  "sleep-everything": {
    title: "Sleep vs everything else",
    subtitle: "Sleep stays large across life; everything else must fit into the remaining waking hours.",
    series: [
      { label: "Sleep", category: "Sleep", value: age => categoryHours(age, "Sleep") },
      { label: "Everything else", category: "Travel", value: age => 24 - categoryHours(age, "Sleep") }
    ]
  }
};

let roomRows = [];
let rhythmRows = [];
let socialRows = [];
let receiptRows = [];
let currentAge = "18-24";
let currentHighlight = "Leisure";
let lockedCategory = null;
let receiptAge = "35-44";
let selectedTradeoff = "work-leisure";
let tooltip;

loadData();

function loadData() {
  Promise.all([
    d3.csv("data/processed/age_room_summary.csv", d3.autoType),
    d3.csv("data/processed/age_daily_rhythm.csv", d3.autoType),
    d3.csv("data/processed/age_social_context.csv", d3.autoType),
    d3.csv("data/processed/life_receipt.csv", d3.autoType),
    d3.json("data/processed/atus_2024_metadata.json")
  ]).then(([rooms, rhythm, social, receipt]) => {
    roomRows = rooms;
    rhythmRows = rhythm;
    socialRows = social;
    receiptRows = receipt;

    prepareAgeData();
    initTooltip();
    renderHeroClock();
    renderHeroMiniLegend();
    renderAgePills();
    renderLifeClock();
    renderClockLegend();
    renderTradeoffChart();
    renderDailyRhythm();
    setupLifeReceipt();
    setupScroll();
    setupTradeoffControls();
    updateLifeStage(currentAge, currentHighlight);

    window.addEventListener("resize", debounce(() => {
      renderHeroClock();
      renderLifeClock();
      renderTradeoffChart();
      renderDailyRhythm();
      applyCategoryHighlight(lockedCategory || currentHighlight);
    }, 150));
  }).catch(error => {
    console.error(error);
    d3.select("#stage-sentence").text("One or more processed data files could not be loaded.");
  });
}

function prepareAgeData() {
  roomRows.forEach(d => {
    d.avg_hours_per_day = +d.avg_hours_per_day;
    d.avg_minutes_per_day = +d.avg_minutes_per_day;
  });
}

function initTooltip() {
  d3.select(".tooltip").remove();
  tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .attr("role", "status")
    .attr("aria-live", "polite");
}

function showTooltip(event, html) {
  tooltip.html(html).classed("is-visible", true);
  moveTooltip(event);
}

function moveTooltip(event) {
  if (!tooltip || !tooltip.classed("is-visible")) return;
  const node = tooltip.node();
  const padding = 16;
  const width = node.offsetWidth || 220;
  const height = node.offsetHeight || 110;
  let left = event.clientX + 18;
  let top = event.clientY + 18;

  if (left + width + padding > window.innerWidth) left = event.clientX - width - 18;
  if (top + height + padding > window.innerHeight) top = event.clientY - height - 18;

  tooltip
    .style("left", `${Math.max(padding, left)}px`)
    .style("top", `${Math.max(padding, top)}px`);
}

function hideTooltip() {
  tooltip.classed("is-visible", false);
}

function renderHeroClock() {
  const container = d3.select("#hero-clock");
  container.html("");
  const width = container.node()?.clientWidth || 520;
  const height = Math.max(230, Math.min(340, width * 0.62));
  const svg = container.append("svg").attr("viewBox", `0 0 ${width} ${height}`);
  const blocks = makeHeroBlocks("35-44");
  const x = d3.scaleBand().domain(blocks.map(d => d.index)).range([24, width - 24]).padding(0.14);
  const y = height / 2;

  svg.append("line")
    .attr("x1", 24)
    .attr("x2", width - 24)
    .attr("y1", y)
    .attr("y2", y)
    .attr("class", "hero-line");

  svg.selectAll("rect")
    .data(blocks)
    .join("rect")
    .attr("class", "hero-hour-block")
    .attr("x", d => x(d.index))
    .attr("y", d => y - 38 - Math.sin(d.index / 47 * Math.PI) * 34)
    .attr("width", x.bandwidth())
    .attr("height", d => 22 + Math.sin(d.index / 47 * Math.PI) * 62)
    .attr("rx", 6)
    .attr("fill", d => colorFor(d.category))
    .attr("tabindex", 0)
    .on("mouseenter focus", (event, d) => {
      showTooltip(event, tooltipHtml(d.category, [
        "Preview day: age 35-44",
        "Each mark is about 30 minutes",
        `${formatPercent(0.5 / 24)} of the day`
      ]));
    })
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", hideTooltip);

  svg.append("text")
    .attr("x", width / 2)
    .attr("y", height - 38)
    .attr("class", "hero-clock-label")
    .text("Colors show how one day gets divided");
}

function renderHeroMiniLegend() {
  renderLegend("#hero-mini-legend", CLOCK_CATEGORIES, {
    itemClass: "mini-legend-item",
    interactive: false
  });
}

function renderAgePills() {
  const pills = d3.select("#age-pills");
  pills.html("");
  pills.selectAll("button")
    .data(AGES)
    .join("button")
    .attr("type", "button")
    .attr("class", d => `age-pill ${d === currentAge ? "is-selected" : ""}`)
    .text(d => formatAge(d))
    .on("click", (event, age) => {
      updateLifeStage(age, lockedCategory || defaultHighlight(age));
    });
}

function renderLifeClock() {
  const container = d3.select("#life-clock");
  container.html("");
  const width = container.node()?.clientWidth || 760;
  const mobile = width < 560;
  const margin = { top: 24, right: 28, bottom: 78, left: 28 };
  const cols = mobile ? 12 : 24;
  const rows = mobile ? 8 : 4;
  const cellGap = mobile ? 5 : 7;
  const cell = Math.max(12, Math.floor((width - margin.left - margin.right - (cols - 1) * cellGap) / cols));
  const height = margin.top + rows * cell + (rows - 1) * cellGap + margin.bottom;
  const svg = container.append("svg").attr("width", width).attr("height", height);

  svg.append("g").attr("class", "time-blocks");
  svg.append("g").attr("class", "clock-axis");
  updateLifeClock(currentAge);
}

function updateLifeClock(age) {
  const container = d3.select("#life-clock");
  const svg = container.select("svg");
  if (svg.empty()) {
    renderLifeClock();
    return;
  }

  const width = container.node()?.clientWidth || 760;
  const mobile = width < 560;
  const margin = { top: 24, right: 28, bottom: 78, left: 28 };
  const cols = mobile ? 12 : 24;
  const rows = mobile ? 8 : 4;
  const cellGap = mobile ? 5 : 7;
  const cell = Math.max(12, Math.floor((width - margin.left - margin.right - (cols - 1) * cellGap) / cols));
  const blocks = makeTimeBlocks(age);

  svg.select("g.time-blocks")
    .selectAll("rect.time-block")
    .data(blocks, d => d.index)
    .join(
      enter => enter.append("rect")
        .attr("class", "time-block")
        .attr("x", d => margin.left + (d.index % cols) * (cell + cellGap))
        .attr("y", d => margin.top + Math.floor(d.index / cols) * (cell + cellGap))
        .attr("width", cell)
        .attr("height", cell)
        .attr("rx", Math.min(8, cell * 0.25))
        .attr("fill", d => colorFor(d.category))
        .attr("tabindex", 0)
        .attr("role", "img")
        .attr("aria-label", d => `${age}, ${d.timeLabel}, ${d.category}`)
        .call(addLifeBlockEvents),
      update => update
        .attr("aria-label", d => `${age}, ${d.timeLabel}, ${d.category}`)
        .call(update => update.transition()
          .duration(520)
          .ease(d3.easeCubicOut)
          .attr("fill", d => colorFor(d.category)))
    );

  const anchors = [
    { hour: 0, label: "12am" },
    { hour: 6, label: "6am" },
    { hour: 12, label: "noon" },
    { hour: 18, label: "6pm" },
    { hour: 24, label: "12am" }
  ];

  const axisY = margin.top + rows * cell + (rows - 1) * cellGap + 34;
  const axisX = d3.scaleLinear()
    .domain([0, 24])
    .range([margin.left + cell / 2, width - margin.right - cell / 2]);
  const axis = svg.select("g.clock-axis").html("");
  axis.append("line")
    .attr("class", "life-clock-axis-line")
    .attr("x1", axisX(0))
    .attr("x2", axisX(24))
    .attr("y1", axisY - 12)
    .attr("y2", axisY - 12);

  anchors.forEach(anchor => {
    axis.append("text")
      .attr("x", axisX(anchor.hour))
      .attr("y", axisY)
      .attr("class", "axis-text")
      .attr("text-anchor", anchor.hour === 0 ? "start" : anchor.hour === 24 ? "end" : "middle")
      .text(anchor.label);
  });

  applyCategoryHighlight(lockedCategory || currentHighlight);
}

function addLifeBlockEvents(selection) {
  selection
    .on("mouseenter focus", (event, d) => {
      if (!lockedCategory) applyCategoryHighlight(d.category);
      showTooltip(event, tooltipHtml(d.category, [
        `Age group: ${formatAge(d.age)}`,
        `Time: ${d.timeLabel}`,
        "Each square represents 15 minutes",
        `${formatPercent(0.25 / 24)} of the day`
      ]));
    })
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", () => {
      if (!lockedCategory) applyCategoryHighlight(currentHighlight);
      hideTooltip();
    });
}

function renderClockLegend() {
  const visibleCategories = groupedRowsForAge(currentAge)
    .filter(d => d.hours > 0.02)
    .map(d => d.category);
  if (lockedCategory && !visibleCategories.includes(lockedCategory)) lockedCategory = null;

  renderLegend("#clock-legend", visibleCategories, {
    itemClass: "legend-item",
    interactive: true,
    lockable: true,
    reset: true
  });
}

function updateLifeStage(age, highlight = defaultHighlight(age)) {
  currentAge = age;
  currentHighlight = highlight;

  d3.selectAll(".step").classed("is-active", function () {
    return this.dataset.age === age;
  });
  d3.selectAll(".age-pill").classed("is-selected", d => d === age);

  d3.select("#stage-pill").text(formatAge(age));
  d3.select("#stage-title").text(`Maya's 24 hours at ${formatAge(age)}`);
  d3.select("#stage-sentence").text(STAGE_COPY[age].sentence);
  d3.select("#maya-age-text").text(age === "65+" ? "65+" : age.split("-")[0]);

  updateAvatarCard(age);
  renderClockLegend();
  updateLifeClock(age);
}

function updateAvatarCard(age) {
  const biggest = biggestCategory(age);
  const squeezed = mostSqueezedCategory(age);
  const yours = categoryHours(age, "Leisure");
  const obligations = obligationHours(age);

  setMetricText("#avatar-age", formatAge(age));
  setMetricText("#avatar-biggest", `${biggest.category} (${formatHours(biggest.hours)})`);
  setMetricText("#avatar-squeezed", `${squeezed.category} (${formatHours(squeezed.hours)})`);
  setMetricText("#avatar-yours", `${formatHours(yours)} of leisure`);
  setMetricText("#avatar-obligations", `${formatHours(obligations)} of work, care, and travel`);
  setMetricText("#avatar-summary", STAGE_COPY[age].summary);
}

function setMetricText(selector, value) {
  const selection = d3.select(selector);
  if (selection.text() === value) return;
  selection.text(value).classed("value-pulse", true);
  window.setTimeout(() => selection.classed("value-pulse", false), 420);
}

function setupScroll() {
  const steps = document.querySelectorAll(".step");
  if (!steps.length || !("IntersectionObserver" in window)) return;

  const observer = new IntersectionObserver(entries => {
    entries
      .filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
      .slice(0, 1)
      .forEach(entry => updateLifeStage(entry.target.dataset.age, entry.target.dataset.highlight));
  }, { threshold: [0.45, 0.65], rootMargin: "-24% 0px -28% 0px" });

  steps.forEach(step => observer.observe(step));
}

function setupTradeoffControls() {
  d3.selectAll(".tradeoff-button").on("click", event => {
    selectedTradeoff = event.currentTarget.dataset.tradeoff;
    d3.selectAll(".tradeoff-button").classed("is-selected", function () {
      return this.dataset.tradeoff === selectedTradeoff;
    });
    updateTradeoffChart(selectedTradeoff);
  });
}

function updateTradeoffChart(mode) {
  selectedTradeoff = mode;
  renderTradeoffChart();
}

function renderTradeoffChart() {
  const container = d3.select("#tradeoff-chart");
  container.html("");
  const width = container.node()?.clientWidth || 900;
  const height = width < 640 ? 430 : 440;
  const margin = { top: width < 560 ? 92 : 66, right: width < 560 ? 22 : 132, bottom: 76, left: width < 560 ? 50 : 86 };
  const svg = container.append("svg").attr("width", width).attr("height", height);
  const config = TRADEOFFS[selectedTradeoff];
  const series = getTradeoffSeries(config);
  const allValues = series.flatMap(s => s.values);
  const x = d3.scalePoint().domain(AGES).range([margin.left, width - margin.right]).padding(0.45);
  const y = d3.scaleLinear()
    .domain([0, Math.max(10, d3.max(allValues, d => d.hours) || 10)])
    .nice()
    .range([height - margin.bottom, margin.top]);
  const line = d3.line().x(d => x(d.age)).y(d => y(d.hours)).curve(d3.curveMonotoneX);

  svg.append("text").attr("x", margin.left).attr("y", 26).attr("class", "chart-title").text(config.title);
  svg.append("text").attr("x", margin.left).attr("y", 48).attr("class", "chart-subtitle").text(config.subtitle);

  svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickFormat(formatAge).tickSize(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll("text").attr("class", "axis-text"));

  svg.append("g")
    .attr("class", "y-axis")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).ticks(4).tickFormat(d => `${d} hrs`).tickSize(-(width - margin.left - margin.right)))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll(".tick line").attr("class", "grid-line"))
    .call(g => g.selectAll("text").attr("class", "axis-text"));

  svg.append("text")
    .attr("class", "axis-title")
    .attr("x", margin.left)
    .attr("y", height - 20)
    .text("Age group");

  if (width < 560) {
    svg.append("text")
      .attr("class", "axis-title")
      .attr("x", margin.left)
      .attr("y", margin.top - 12)
      .text("Hours per day");
  } else {
    svg.append("text")
      .attr("class", "axis-title")
      .attr("transform", `translate(18,${margin.top}) rotate(-90)`)
      .text("Hours per day");
  }

  const focusLine = svg.append("line")
    .attr("class", "focus-guide")
    .attr("y1", margin.top)
    .attr("y2", height - margin.bottom)
    .attr("opacity", 0);

  const group = svg.selectAll("g.trade-series")
    .data(series)
    .join("g")
    .attr("class", "trade-series")
    .attr("data-label", d => d.label);

  group.append("path")
    .attr("class", "trade-line")
    .attr("fill", "none")
    .attr("stroke", d => colorFor(d.category))
    .attr("stroke-width", 4)
    .attr("stroke-linecap", "round")
    .attr("d", d => line(d.values))
    .on("mouseenter focus", (event, d) => highlightTradeSeries(d.label))
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", clearTradeSeriesHighlight);

  group.selectAll("circle")
    .data(d => d.values.map(value => ({ ...value, label: d.label, category: d.category })))
    .join("circle")
    .attr("class", "trade-point")
    .attr("cx", d => x(d.age))
    .attr("cy", d => y(d.hours))
    .attr("r", 5.5)
    .attr("fill", d => colorFor(d.category))
    .attr("tabindex", 0)
    .on("mouseenter focus", (event, d) => {
      highlightTradeSeries(d.label);
      focusLine.attr("x1", x(d.age)).attr("x2", x(d.age)).attr("opacity", 1);
      showTooltip(event, tooltipHtml(d.label, [
        `Age group: ${formatAge(d.age)}`,
        `${formatHours(d.hours)} per day`,
        `About ${formatPercent(d.hours / 24)} of the day`
      ]));
    })
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", () => {
      clearTradeSeriesHighlight();
      focusLine.attr("opacity", 0);
      hideTooltip();
    });

  group.selectAll("text.end-label")
    .data(d => [d.values[d.values.length - 1]].map(value => ({ ...value, label: d.label, category: d.category })))
    .join("text")
    .attr("class", "end-label")
    .attr("x", d => width < 560 ? x(d.age) - 4 : x(d.age) + 10)
    .attr("y", d => y(d.hours) + 4)
    .attr("text-anchor", width < 560 ? "end" : "start")
    .attr("fill", d => colorFor(d.category))
    .text(d => width < 560 ? `${formatHours(d.hours)}` : `${d.label} ${formatHours(d.hours)}`);
}

function highlightTradeSeries(label) {
  d3.selectAll(".trade-series").classed("is-muted", function (d) {
    return d.label !== label;
  });
  d3.selectAll(".trade-series").classed("is-focused", function (d) {
    return d.label === label;
  });
}

function clearTradeSeriesHighlight() {
  d3.selectAll(".trade-series").classed("is-muted", false).classed("is-focused", false);
  hideTooltip();
}

function renderDailyRhythm() {
  const container = d3.select("#rhythm-chart");
  container.html("");
  const width = container.node()?.clientWidth || 960;
  const mobile = width < 560;
  const height = width < 640 ? 400 : 410;
  const margin = { top: 72, right: mobile ? 16 : 30, bottom: mobile ? 62 : 68, left: mobile ? 54 : 86 };
  const svg = container.append("svg").attr("width", width).attr("height", height);
  const x = d3.scaleBand().domain(d3.range(24)).range([margin.left, width - margin.right]).paddingInner(0.1);
  const y = d3.scaleBand().domain(AGES).range([margin.top, height - margin.bottom]).paddingInner(0.18);
  const cells = AGES.flatMap(age => dominantRhythm(age));
  const visibleCategorySet = new Set(cells.map(d => d.category));
  const visibleCategories = CATEGORY_ORDER.filter(category => visibleCategorySet.has(category));

  svg.append("text")
    .attr("x", margin.left)
    .attr("y", 28)
    .attr("class", mobile ? "chart-title chart-title-small" : "chart-title")
    .text("Dominant activity by hour");

  if (mobile) {
    svg.append("text")
      .attr("x", margin.left)
      .attr("y", 50)
      .attr("class", "chart-subtitle")
      .text("Each cell shows the dominant activity");
    svg.append("text")
      .attr("x", margin.left)
      .attr("y", 64)
      .attr("class", "chart-subtitle")
      .text("for that age group at that hour.");
  } else {
    svg.append("text")
      .attr("x", margin.left)
      .attr("y", 50)
      .attr("class", "chart-subtitle")
      .text("Each cell shows the dominant activity for that age group at that hour.");
  }

  const cellGroup = svg.append("g").attr("class", "rhythm-cells");
  cellGroup.selectAll("rect.rhythm-cell")
    .data(cells)
    .join("rect")
    .attr("class", "rhythm-cell")
    .attr("x", d => x(d.hour))
    .attr("y", d => y(d.age_group))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("rx", 5)
    .attr("fill", d => colorFor(d.category))
    .attr("tabindex", 0)
    .attr("aria-label", d => `${formatAge(d.age_group)}, ${formatHour(d.hour)}, ${d.category}`)
    .on("mouseenter focus", (event, d) => {
      highlightRhythmCell(d.age_group, d.hour);
      showTooltip(event, tooltipHtml(d.category, [
        `Age group: ${formatAge(d.age_group)}`,
        `Hour: ${formatHour(d.hour)}`,
        `Dominant activity: ${d.category}`,
        `Share of hour: ${formatPercent(d.share)}`
      ]));
    })
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", () => {
      clearRhythmHighlight();
      hideTooltip();
    });

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickValues([0, 6, 12, 18, 23]).tickFormat(d => d === 23 ? "12am" : formatHour(d)).tickSize(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll("text").attr("class", "axis-text"));

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickFormat(formatAge).tickSize(0))
    .call(g => g.select(".domain").remove())
    .call(g => g.selectAll("text").attr("class", "axis-text"));

  svg.append("text")
    .attr("class", "axis-title")
    .attr("x", (margin.left + width - margin.right) / 2)
    .attr("y", height - 20)
    .attr("text-anchor", "middle")
    .text("Hour of day");

  if (mobile) {
    svg.append("text")
      .attr("class", "axis-title")
      .attr("x", margin.left)
      .attr("y", margin.top - 10)
      .text("Age group");
  } else {
    svg.append("text")
      .attr("class", "axis-title")
      .attr("transform", `translate(18,${(margin.top + height - margin.bottom) / 2}) rotate(-90)`)
      .attr("text-anchor", "middle")
      .text("Age group");
  }

  const legend = container.append("div").attr("class", "chart-legend rhythm-legend");
  renderLegend(legend, visibleCategories, {
    itemClass: "chart-legend-item",
    interactive: false
  });
  container.append("p")
    .attr("class", "legend-note")
    .text("Household/Care may still appear in the receipt because the receipt shows total time across the whole day. This grid only shows the activity that is most dominant in each hour, so smaller activities may not appear even when they add up over the day.");
  container.append("p")
    .attr("class", "legend-note")
    .text("Legend shows only activities that appear as the dominant activity in this grid.");
}

function highlightRhythmCell(age, hour) {
  d3.selectAll(".rhythm-cell")
    .classed("is-muted", d => d.age_group !== age && d.hour !== hour)
    .classed("is-focused", d => d.age_group === age && d.hour === hour);
}

function clearRhythmHighlight() {
  d3.selectAll(".rhythm-cell").classed("is-muted", false).classed("is-focused", false);
}

function setupLifeReceipt() {
  d3.select("#receipt-age")
    .selectAll("option")
    .data(AGES)
    .join("option")
    .attr("value", d => d)
    .text(formatAge);

  d3.select("#receipt-age")
    .property("value", receiptAge)
    .on("change", event => {
      receiptAge = event.target.value;
      updateLifeReceipt();
    });

  updateLifeReceipt();
}

function updateLifeReceipt() {
  renderLifeReceipt(receiptAge);
}

function renderLifeReceipt(age = receiptAge) {
  const receipt = d3.select("#life-receipt");
  const rows = receiptRowsForAge(age);
  const yours = categoryHours(age, "Leisure");
  const obligations = obligationHours(age);
  const recovering = categoryHours(age, "Sleep");

  receipt.html(`
    <div class="receipt-head">
      <p>Your 24-Hour Receipt</p>
      <h3>Maya at ${formatAge(age)}</h3>
      <span>Weighted 2024 ATUS average</span>
    </div>
    ${rows.map(row => `
      <div class="receipt-row" data-category="${row.category}" style="--row-color:${colorFor(row.category)}">
        <span class="receipt-swatch"></span>
        <div>
          <strong>${row.label}</strong>
          <small>${row.emotion}</small>
        </div>
        <span class="receipt-hours">${formatHours(row.hours)}</span>
        <em>${formatPercent(row.hours / 24)}</em>
      </div>
    `).join("")}
    <div class="receipt-summary">
      <p><strong>Things that felt like yours:</strong> ${formatHours(yours)} of leisure and self-directed time.</p>
      <p><strong>Obligations:</strong> ${formatHours(obligations)} spent on work, school, household work, care, and travel.</p>
      <p><strong>Recovery:</strong> ${formatHours(recovering)} spent sleeping and taking care of the body.</p>
    </div>
    <p class="receipt-note">Social time uses the ATUS social-context file, so it can overlap with the activity categories above.</p>
  `);

  receipt.selectAll(".receipt-row")
    .on("mouseenter focus", (event) => {
      const category = event.currentTarget.dataset.category;
      event.currentTarget.classList.add("is-focused");
      showTooltip(event, tooltipHtml(category, [
        CATEGORY[category]?.description || "Mapped from the closest processed category",
        "Rows update instantly when the age group changes"
      ]));
    })
    .on("mousemove", moveTooltip)
    .on("mouseleave blur", (event) => {
      event.currentTarget.classList.remove("is-focused");
      hideTooltip();
    });
}

function receiptRowsForAge(age) {
  // The processed activity file has seven raw ATUS groups. These rows combine them into story buckets.
  return [
    receiptRow(age, "Sleep"),
    receiptRow(age, "Work/Education"),
    receiptRow(age, "Household/Care"),
    receiptRow(age, "Leisure"),
    {
      label: "Social",
      category: "Social",
      emotion: CATEGORY.Social.description,
      hours: socialHours(age, "Together")
    },
    receiptRow(age, "Travel")
  ];
}

function receiptRow(age, category) {
  return {
    label: category,
    category,
    emotion: CATEGORY[category].description,
    hours: categoryHours(age, category)
  };
}

function makeHeroBlocks(age) {
  return makeTimeBlocks(age)
    .filter(d => d.index % 2 === 0)
    .map((d, i) => ({ ...d, index: i }));
}

function makeTimeBlocks(age) {
  const rows = groupedRowsForAge(age).filter(d => CLOCK_CATEGORIES.includes(d.category));
  const cumulative = [];
  let cursor = 0;
  rows.forEach(row => {
    const start = cursor;
    cursor += row.hours;
    cumulative.push({ category: row.category, start, end: cursor });
  });

  return d3.range(96).map(index => {
    const hour = index / 4;
    const match = cumulative.find(d => hour >= d.start && hour < d.end) || cumulative[cumulative.length - 1];
    return {
      index,
      age,
      category: match.category,
      timeLabel: formatQuarterHour(index)
    };
  });
}

function getTradeoffSeries(config) {
  return config.series.map(series => ({
    label: series.label,
    category: series.category,
    values: AGES.map(age => ({ age, hours: series.value(age) }))
  }));
}

function dominantRhythm(age) {
  return d3.range(24).map(hour => {
    const rows = rhythmRows.filter(d => d.age_group === age && d.hour === hour);
    const top = d3.greatest(rows, d => d.share_of_hour);
    const rawRoom = top?.room || "Other";
    return {
      age_group: age,
      hour,
      room: rawRoom,
      category: RAW_TO_CATEGORY[rawRoom] || "Other",
      share: top?.share_of_hour || 0
    };
  });
}

function renderLegend(container, categories, options = {}) {
  const target = typeof container === "string" ? d3.select(container) : container;
  const itemClass = options.itemClass || "legend-item";
  const interactive = options.interactive !== false;
  const tag = interactive ? "button" : "div";

  target.html("");

  const items = target.selectAll(tag)
    .data(categories)
    .join(tag)
    .attr("class", itemClass)
    .attr("data-category", d => d)
    .html(category => `<span style="background:${colorFor(category)}"></span>${category}`);

  if (interactive) {
    items
      .attr("type", "button")
      .on("mouseenter focus", (event, category) => {
        if (!lockedCategory) applyCategoryHighlight(category);
      })
      .on("mouseleave blur", () => {
        if (!lockedCategory) applyCategoryHighlight(currentHighlight);
      });
  }

  if (options.lockable) {
    items.on("click", (event, category) => {
      lockedCategory = lockedCategory === category ? null : category;
      applyCategoryHighlight(lockedCategory || currentHighlight);
    });
  }

  if (options.reset) {
    target.append("button")
      .attr("type", "button")
      .attr("class", "legend-reset")
      .text("Reset highlight")
      .on("click", clearCategoryHighlight);
  }

  applyCategoryHighlight(lockedCategory || currentHighlight);
}

function applyCategoryHighlight(category) {
  const active = category || null;
  d3.selectAll(".time-block")
    .classed("is-muted", d => active && d.category !== active)
    .classed("is-focused", d => active && d.category === active);
  d3.selectAll(".legend-item")
    .classed("is-selected", function (d) {
      return lockedCategory ? d === lockedCategory : d === active;
    });
}

function clearCategoryHighlight() {
  lockedCategory = null;
  applyCategoryHighlight(currentHighlight);
}

function biggestCategory(age) {
  return d3.greatest(groupedRowsForAge(age), d => d.hours);
}

function mostSqueezedCategory(age) {
  return d3.least(groupedRowsForAge(age).filter(d => d.hours >= 0.05), d => d.hours);
}

function groupedRowsForAge(age) {
  return CLOCK_CATEGORIES.map(category => ({
    category,
    hours: categoryHours(age, category)
  }));
}

function categoryHours(age, category) {
  return d3.sum(CATEGORY[category]?.rooms || [], room => valueFor(age, room)?.avg_hours_per_day || 0);
}

function obligationHours(age) {
  return categoryHours(age, "Work/Education") + categoryHours(age, "Household/Care") + categoryHours(age, "Travel");
}

function socialHours(age, context) {
  return socialRows.find(d => d.age_group === age && d.social_context === context)?.avg_hours_per_day || 0;
}

function valueFor(age, room) {
  return roomRows.find(d => d.age_group === age && d.room === room);
}

function defaultHighlight(age) {
  return d3.greatest(groupedRowsForAge(age).filter(d => d.category !== "Sleep"), d => d.hours)?.category || "Leisure";
}

function colorFor(category) {
  return CATEGORY[category]?.color || CATEGORY.Other.color;
}

function tooltipHtml(title, lines) {
  return `
    <strong>${title}</strong>
    ${lines.map(line => `<span>${line}</span>`).join("")}
  `;
}

function formatAge(age) {
  return age.replace("-", "–");
}

function formatHours(value) {
  return Number.isFinite(value) ? `${d3.format(".1f")(value)} hrs` : "0.0 hrs";
}

function formatPercent(value) {
  return Number.isFinite(value) ? d3.format(".0%")(value) : "0%";
}

function formatHour(hour) {
  if (hour === 0 || hour === 24) return "12am";
  if (hour === 12) return "noon";
  if (hour < 12) return `${hour}am`;
  return `${hour - 12}pm`;
}

function formatQuarterHour(index) {
  const hour = Math.floor(index / 4);
  const minute = (index % 4) * 15;
  const suffix = hour < 12 ? "am" : "pm";
  const hour12 = hour % 12 || 12;
  return `${hour12}:${String(minute).padStart(2, "0")}${suffix}`;
}

function debounce(fn, wait) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), wait);
  };
}
