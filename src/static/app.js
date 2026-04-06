document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  let activitiesData = {}; // Store activities data for availability check

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();
      activitiesData = activities; // Store the activities data

      // Clear loading message
      activitiesList.innerHTML = "";

      // Clear existing options except the first one
      while (activitySelect.options.length > 1) {
        activitySelect.remove(1);
      }

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        const participantsHtml = details.participants.length > 0
          ? `<ul class="participants-list">${details.participants.map(email => `<li><span>${email}</span><button class="delete-btn" data-activity="${name}" data-email="${email}" title="Remove participant">🗑</button></li>`).join("")}</ul>`
          : `<p class="no-participants">No participants yet</p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants">
            <strong>Participants:</strong>
            ${participantsHtml}
          </div>
        `;

        activitiesList.appendChild(activityCard);
        
        // Add delete button event listeners
        const deleteButtons = activityCard.querySelectorAll(".delete-btn");
        deleteButtons.forEach(button => {
          button.addEventListener("click", handleDeleteParticipant);
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Function to check availability and update button state
  function checkActivityAvailability() {
    const selectedActivity = activitySelect.value;
    const submitBtn = signupForm.querySelector("button[type='submit']");
    
    if (selectedActivity && activitiesData[selectedActivity]) {
      const activity = activitiesData[selectedActivity];
      const spotsLeft = activity.max_participants - activity.participants.length;
      
      if (spotsLeft <= 0) {
        submitBtn.disabled = true;
        submitBtn.style.opacity = "0.5";
        submitBtn.style.cursor = "not-allowed";
        submitBtn.title = "Slot closed, Kindly wait for future openings";
      } else {
        submitBtn.disabled = false;
        submitBtn.style.opacity = "1";
        submitBtn.style.cursor = "pointer";
        submitBtn.title = "";
      }
    }
  }

  // Event listener for activity selection
  activitySelect.addEventListener("change", checkActivityAvailability);

  // Handle delete participant
  async function handleDeleteParticipant(event) {
    event.preventDefault();
    const activity = event.target.getAttribute("data-activity");
    const email = event.target.getAttribute("data-email");

    // Show confirmation dialog
    if (!window.confirm(`Are you sure you want to remove ${email} from ${activity}?`)) {
      return; // Cancel the deletion operation
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        messageDiv.textContent = `Removed ${email} from ${activity}`;
        messageDiv.className = "success";
        messageDiv.classList.remove("hidden");
        
        // Refresh activities list
        fetchActivities();
        checkActivityAvailability();
        
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 5000);
      } else {
        const result = await response.json();
        messageDiv.textContent = result.detail || "Failed to remove participant";
        messageDiv.className = "error";
        messageDiv.classList.remove("hidden");
      }
    } catch (error) {
      messageDiv.textContent = "Failed to remove participant. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error removing participant:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        messageDiv.classList.remove("hidden");
        signupForm.reset();
        
        // Refresh activities list to show updated participants
        fetchActivities();
        checkActivityAvailability();
        
        // Hide message after 5 seconds
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 5000);
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
        messageDiv.classList.remove("hidden");
        
        // Hide message after 5 seconds
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 5000);
      }
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
  checkActivityAvailability();
});
