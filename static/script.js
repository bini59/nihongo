function downlaod_pdf(url) {
    const api_key = document.getElementById('api-key-input').value;
    fetch(`http://localhost:8000/pdf/download_article_pdf?url=${url}&api_key=${api_key}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
}

function openTab(event, tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tabContent => {
        tabContent.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show the current tab and add active class
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');


    // Load the news if not loaded
    if (document.getElementById(tabName).children.length === 0) {
        fetch(`http://localhost:8000/news/get_articles?category=${tabName}`)
            .then(response => response.json())
            .then(data => {
                for (let article of data) {
                    add_news(article, tabName);
                }
            });
    }
}

function init() {
    const categories = ["top-picks", "domestic", "world", "business", "entertainment", "sports", "it", "science", "local"];
    for (let category of categories) {
        const tabContent = document.createElement('div');
        tabContent.classList.add('tab-content');
        if (category === "top-picks") {
            tabContent.classList.add('active');
        }
        tabContent.id = category;
        document.getElementsByClassName('content')[0].appendChild(tabContent);
    }
}

function add_news(data, category) {
    // let layout = `                
    // <div class="row">
    //     <div class="pic">Pic</div>
    //     <div class="title">
    //         <h2>${data.title}</h2>
    //         <button class="inner-button">공부하자!</button>
    //     </div>
    // </div>`

    const tabContent = document.createElement('div');
    tabContent.classList.add('row');
    tabContent.innerHTML = `
        <div class="pic">Pic</div>
    `;
    const title = document.createElement('div');
    title.classList.add('title');
    title.innerHTML = `<h2>${data.title}</h2>`;
    const button = document.createElement('button');
    button.classList.add('inner-button');
    button.innerHTML = "공부하자!";
    button.addEventListener('click', () => {
        downlaod_pdf(data.url);  
    });
    title.appendChild(button);

    tabContent.appendChild(title);

    document.getElementById(category).appendChild(tabContent);
}

document.addEventListener('DOMContentLoaded', () => {
    init()

    fetch(`http://localhost:8000/news/get_articles?category=top-picks`)
    .then(response => response.json())
    .then(data => {
        for (let article of data) {
            add_news(article, 'top-picks');
        }
    });
});