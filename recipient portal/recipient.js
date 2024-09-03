// Function to show the tracking details and hide the login section
function showTrackingDetails() {
    document.getElementById("login-container").style.display = "none";
    document.getElementById("tracking-section").style.display = "flex"; // Flex display for proper layout
}

let currentSection = 0;
const sections = document.querySelectorAll('.details > div'); // Get all sections within the details container
const nextBtn = document.getElementById('nextBtn'); // Next button for navigating between sections
const prevBtn = document.getElementById('prevBtn'); // Previous button for navigating back

let selectedDate = null;
let selectedTimeSlot = null;

function showNext() {
    if (currentSection < sections.length - 1) {
        sections[currentSection].style.display = 'none'; // Hide the current section
        currentSection++; // Increment to the next section
        sections[currentSection].style.display = 'block'; // Show the next section
        if (currentSection === 2) { // If moving to the third section
            displaySelectedInfo(); // Display selected date and time slot
        }
    }
    updateButtons(); // Update button visibility
}


function updateButtons() {
    nextBtn.style.display = currentSection === sections.length - 1 ? 'none' : 'block';
    prevBtn.style.display = currentSection === 0 ? 'none' : 'block';
}

function displaySelectedInfo() {
    document.getElementById('selectedDate').textContent = selectedDate ? selectedDate.toLocaleDateString() : 'Not selected';
    document.getElementById('selectedTimeSlot').textContent = selectedTimeSlot || 'Not selected';
}

updateButtons();  // Initialize button visibility based on the current section

document.addEventListener("DOMContentLoaded", function() {
    const daysContainer = document.getElementById('days');
    const monthYear = document.getElementById('currentMonth');
    let currentDate = new Date();

    function renderCalendar() {
        daysContainer.innerHTML = '';
        monthYear.textContent = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });

        let firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
        let daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();

        // Display blank spaces for days of the previous month
        for (let i = 0; i < firstDay; i++) {
            daysContainer.innerHTML += '<div class="empty-day"></div>';
        }

        // Render days of the current month
        for (let i = 1; i <= daysInMonth; i++) {
            daysContainer.innerHTML += `<div class="day" onclick="selectDate(${i})">${i}</div>`;
        }
    }

    // Event listeners for previous and next month buttons
    document.getElementById('prevMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById('nextMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    renderCalendar();  // Render calendar on page load

    // Handle date selection
    window.selectDate = function(day) {
        document.querySelectorAll('.day').forEach(el => el.classList.remove('selected'));
        selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
        document.querySelector(`.day:nth-child(${day + new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()})`).classList.add('selected');
    }

    // Handle time slot selection
    document.querySelectorAll('.slot').forEach(slot => {
        slot.addEventListener('click', function() {
            console.log('Slot clicked:', this.textContent); // Debug statement
            document.querySelectorAll('.slot').forEach(s => s.classList.remove('selected'));
            selectedTimeSlot = this.textContent;
            slot.classList.add('selected');
        });
    });
});
