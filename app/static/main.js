// Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultSection = document.getElementById('resultSection');
    const resultPre = document.getElementById('result');
// ...existing code...
    // --- Mock Functions for Tool Logic ---
    // Function to simulate showing the loading spinner and then a result
  function showLoadingAndResult(promptText) {
    resultSection.classList.add('hidden');
    // Simulate a network request
    setTimeout(() => {
      loadingSpinner.classList.add('hidden');
      resultPre.textContent = promptText;
      resultSection.classList.remove('hidden');
    }, 1500); // 1.5 second delay
  }
  /**
   * Asynchronously generates a prompt based on the user's task description and selected provider.
   * Shows a loading spinner while fetching data from the server, and updates the result element with
   * the response prompt or an error message. Displays a copy button if the prompt generation is successful.
   * 
   * Elements:
   * - task: The task description input by the user.
   * - provider: The selected AI provider.
   * - resultElement: The element where the resulting prompt or error message is displayed.
   * - copyButtonContainer: The element containing the copy button, shown if a prompt is successfully generated.
   * - loadingSpinner: The spinner displayed during the API call.
   * - generateBtn: The button that triggers prompt generation, disabled during the call.
   * 
   * API:
   * - POST /generate: Expects a JSON body with 'task' and 'provider' fields, returns a prompt or error.
   */
    async function generatePrompt() {
      const task = document.getElementById('task').value;
      const provider = document.getElementById('provider').value;
      const generateBtn = document.querySelector('button[onclick="generatePrompt()"]');
      loadingSpinner.classList.remove('hidden');
      generateBtn.disabled = true;
      generateBtn.classList.add('opacity-50', 'cursor-not-allowed');
      try {
        const baseUrl = window.location.origin; // Gets current domain automatically
        const response = await fetch(`${baseUrl}/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ task, provider })
        });
        const data = await response.json();
        const output = data.prompt || data.error || "❌ Unexpected error";
        // Remove "Review and Optimization:" and everything after it
        // Remove "Review" and everything after it, if present
        const reviewMatch = output.match(/Review[\s\S]*/);
        if (reviewMatch) {
          output = output.substring(0, reviewMatch.index).trim();
        }        
        showLoadingAndResult(output);
      } catch (err) {
        resultPre.innerText = "❌ Unable to reach server. Check console.";
        console.error(err);
      } finally {
        // End: hide spinner, re-enable button
        loadingSpinner.classList.add('hidden');
        generateBtn.disabled = false;
        generateBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }
    async function generateShortPrompt() {
	    const task = document.getElementById('task').value;
	    const provider = document.getElementById('provider').value;
	    const generateShortBtn = document.querySelector('button[onclick="generateShortPrompt()"]');
	    // Start: show spinner, disable button
	    loadingSpinner.classList.remove('hidden');
	    generateShortBtn.disabled = true;
	    generateShortBtn.classList.add('opacity-50', 'cursor-not-allowed');
	    try {
		    const baseUrl = window.location.origin;
		    const response = await fetch(`${baseUrl}/generate-short`, {
		      method: 'POST',
		      headers: { 'Content-Type': 'application/json' },
		      body: JSON.stringify({ task, provider })
		  });
		  const data = await response.json();
		  let output = data.prompt || data.error || "❌ Unexpected error";
		  showLoadingAndResult(output);
	  } catch (err) {
		  resultElement.innerText = "❌ Unable to reach server. Check console.";
		  console.error(err);
	  } finally {
		  loadingSpinner.classList.add('hidden');
		  generateShortBtn.disabled = false;
		  generateShortBtn.classList.remove('opacity-50', 'cursor-not-allowed');
	  }
	}    
  // Function to copy result to clipboard
  function copyToClipboard() {
    const textToCopy = resultPre.textContent;
    const textArea = document.createElement("textarea");
    // Use a temporary textarea to copy text to clipboard
    textArea.value = textToCopy;
    document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        alert('Prompt copied to clipboard!');
      } catch (err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy prompt.');
      }
    document.body.removeChild(textArea);
  }