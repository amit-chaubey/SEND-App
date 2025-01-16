// Event listener for form submission (Start button)
document.getElementById("spelling-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const focusSound = document.getElementById("focus-sound").value.trim().toLowerCase();
    const difficultyLevel = document.getElementById("difficulty-level").value;

    fetchNextWord(focusSound, difficultyLevel);
});

// Function to display the flashcard with the word
function displayFlashcard(word) {
    const flashcard = document.getElementById("flash-word");
    const typingContainer = document.getElementById("typing-container");
    const typingInput = document.getElementById("user-word");
    const nextButton = document.getElementById("next-word");

    flashcard.textContent = word;
    typingContainer.style.display = "flex";
    typingInput.value = "";
    typingInput.focus();
    typingContainer.dataset.currentWord = word;

    // Show the Next button if hidden
    nextButton.style.display = "inline-block";
}

// Event listener for the Submit button click
document.getElementById("submit-word").addEventListener("click", validateWord);

// Event listener for Enter key submission
document.getElementById("user-word").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        validateWord();
    }
});

// Event listener for the Next button
document.getElementById("next-word").addEventListener("click", function () {
    const focusSound = document.getElementById("focus-sound").value;
    const difficultyLevel = document.getElementById("difficulty-level").value;

    document.getElementById("feedback").textContent = ""; // Clear feedback
    fetchNextWord(focusSound, difficultyLevel); // Fetch the next word
});

// Function to validate the user's input
async function validateWord() {
    const userWord = document.getElementById("user-word").value.trim().toLowerCase();
    const correctWord = document.getElementById("typing-container").dataset.currentWord;
    const feedback = document.getElementById("feedback");

    if (userWord === correctWord) {
        feedback.innerHTML = `<p style="color: green; font-weight: bold;">🎉 Correct! Great job! 🎉</p>`;
        await updateLeaderboard(true);
    } else {
        feedback.innerHTML = `<p style="color: red; font-weight: bold;">❌ Incorrect. The correct word was "${correctWord}". ❌</p>`;
        await updateLeaderboard(false);
    }

    // Disable Submit button to prevent multiple submissions
    document.getElementById("submit-word").disabled = true;
}

// Function to fetch the next word
function fetchNextWord(focusSound, difficultyLevel) {
    fetch("/word/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            focus_sound: focusSound,
            difficulty_level: parseInt(difficultyLevel),
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.word) {
                const sanitizedWord = data.word.trim().toLowerCase();
                displayFlashcard(sanitizedWord);

                // Re-enable the Submit button
                document.getElementById("submit-word").disabled = false;
            } else {
                document.getElementById("feedback").innerHTML = `<p>Error: ${data.error}</p>`;
            }
        })
        .catch((error) => {
            document.getElementById("feedback").innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Function to update the leaderboard
async function updateLeaderboard(isCorrect) {
    try {
        const response = await fetch("/score/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ correct: isCorrect }),
        });

        if (response.ok) {
            const leaderboardResponse = await fetch("/score/leaderboard");
            const leaderboardData = await leaderboardResponse.json();
            const leaderboardContent = document.getElementById("leaderboard-content");

            leaderboardContent.innerHTML = ""; // Clear existing leaderboard
            leaderboardData.leaderboard.forEach((user) => {
                const entry = document.createElement("div");
                entry.textContent = `${user.username}: ${user.total_score}`;
                leaderboardContent.appendChild(entry);
            });
        }
    } catch (error) {
        console.error("Error updating leaderboard:", error);
    }
}
