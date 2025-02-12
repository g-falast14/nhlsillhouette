document.addEventListener("DOMContentLoaded", function() {
    let guessInput = document.getElementById("player-guess");
    let submitButton = document.getElementById("submit-btn");
    let resultDisplay = document.getElementById("result");
    let nextPlayerButton = document.getElementById("next-player-btn");

    /* get user input */
    submitButton.addEventListener("click", function(){
        let userGuess = guessInput.value.trim().toLowerCase();
        let correctAnswer = guessInput.dataset.correctguess.toLowerCase();
        let resultDisplay = document.getElementById("result");

        if (userGuess == correctAnswer) {
            resultDisplay.innerHTML = "Correct!";
            resultDisplay.classList.add("text-success");
        } else {
            resultDisplay.innerHTML = "Wrong! Try again.";
            resultDisplay.classList.add("text-danger");
        }
    });

    /* Function to grab new player from api and load it */
    function loadNewPlayer() {
        fetch("/get-new-player")
            .then(response => response.json())
            .then(player => {
                console.log("New player data: ", player) // debugging

                // extract new json player details
                let fullName = `${player.firstName.default} ${player.lastName.default}`;
                let newHeadshotUrl = player.headshot;

                // update image and correct guess
                let playerImage = document.getElementById("player-image");
                let guessInput = document.getElementById("player-guess");

                playerImage.src = newHeadshotUrl;
                guessInput.dataset.correctguess = fullName;

                // clear previous results and reset input field
                document.getElementById("result").innerHTML = "";
                guessInput.value = "";
            })

    }

    nextPlayerButton.addEventListener("click", function() {
        console.log("Fetching new player...");
        loadNewPlayer();
        console.log("Successfully grabbed new player");
    })

});