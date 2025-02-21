document.addEventListener("DOMContentLoaded", function () {
    const yearSelect = document.getElementById("year");
    const eventSelect = document.getElementById("event");
    const eventList = document.getElementById("eventList");
    const modal = document.getElementById("modal");
    const modalBody = document.getElementById("modalBody");
    const closeModal = document.getElementById("closeModal");

    const eventData = {
        "2023": {
            "A": [
                { title: "20/11", media: "https://i.ibb.co/6RzTPx6J/image.png"},
                { title: "20/11", media: "https://i.ibb.co/8g7tdD32/image.png" },
            ],
            "B": [
                { title: "Ảnh", media: "image3.jpg" },
                { title: "Video", media: "video3.mp4" },
            ],
            "C": [
                { title: "Ảnh", media: "image5.jpg" },
                { title: "Video", media: "video6.mp4" }
            ]
        },
        "2024": {
            "A": [
                { title: "Hội trại", media: "https://i.imgur.com/Pq6Msfw.jpeg" },
                { title: "Hội trại", media: "https://i.ibb.co/VpCHYyQZ/image.png" },
                { title: "Hội trại", media: "https://i.ibb.co/CxmCY6y/image.png" }
            ],
            "B": [
                { title: "Cuối năm", media: "https://i.ibb.co/wrQg0K38/image.png" },
                { title: "Cuối năm", media: "https://i.ibb.co/wrQg0K38/image.png" },
            ],
            "C": [
                { title: "Làm trại", media: "https://imgur.com/DbfFb3x.jpeg" },
                { title: "Làm trại", media: "https://imgur.com/e70u7ht.jpeg" }
            ]
        },
        "2025": {
            "A": [
                { title: "Boy Day", media: "https://i.imgur.com/zCjvfFm.jpeg" },
                { title: "Boy Day", media: "https://i.imgur.com/MgE5Zt1.jpeg" },
                { title: "Boy Day", media: "https://i.imgur.com/LAlTgQi.jpeg" }
            ],
            "B": [
                { title: "Sinh nhật cô", media: "https://i.ibb.co/WSxHRfR/image.png" },
                { title: "Sinh nhật cô", media: "https://ibb.co/2bm5xqK/image.png" },
            ],
            "C": [
                { title: "20/11", media: "https://i.ibb.co/xSkCmhBz/image.png" },,
                { title: "20/11 - Video", media: "video20-11.mp4" }
            ]
        }
    };
    


    function updateEvents() {
        eventList.innerHTML = "";
        const year = yearSelect.value;
        const event = eventSelect.value;
        if (!eventData[year] || !eventData[year][event]) return;

        eventData[year][event].forEach(evt => {
            const div = document.createElement("div");
            div.className = "event-box";
            div.innerHTML = `<img src="${evt.media.includes('.mp4') ? 'https://i.ibb.co/WSxHRfR/image.png' : evt.media}" 
                             class="event-thumbnail" onclick="showModal('${evt.media}')">
                             <div class="event-title">${evt.title}</div>`;
            eventList.appendChild(div);
        });
    }

    window.showModal = function (media) {
        modalBody.innerHTML = media.includes('.mp4') 
            ? `<video controls autoplay><source src="${media}" type="video/mp4"></video>` 
            : `<img src="${media}">`;
        modal.style.display = "flex";
    };

    closeModal.onclick = () => modal.style.display = "none";
    modal.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };
    yearSelect.onchange = updateEvents;
    eventSelect.onchange = updateEvents;

    updateEvents();
});
