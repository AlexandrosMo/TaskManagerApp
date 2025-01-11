let balance = 0;

// Toggle expense categories visibility based on selected category
document.getElementById("category").addEventListener("change", function () {
    const expenseCategories = document.getElementById("expense-categories");
    if (this.value === "expense") {
        expenseCategories.style.display = "block";
    } else {
        expenseCategories.style.display = "none";
    }
});

// Handle form submission
document.getElementById("transaction-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Fetch form values
    const description = document.getElementById("description").value;
    const amount = parseFloat(document.getElementById("amount").value); // Διόρθωση στο parseFloat
    const category = document.getElementById("category").value;
    const expenseCategory = document.getElementById("expense-category").value;

    // Validate input
    if (!description || isNaN(amount) || amount === 0) {
        alert("Please fill in all fields correctly with a valid amount.");
        return;
    }

    console.log("Before balance update:", balance); // Debug log

    // Update balance
    if (category === "income") {
        balance += amount;
    } else if (category === "expense") {
        balance -= amount;
    }

    console.log("After balance update:", balance); // Debug log

    // Update balance display
    document.getElementById("balance-display").innerText = `$${balance.toFixed(2)}`;

    // Add transaction log entry
    const logEntries = document.getElementById("log-entries");
    const logEntry = document.createElement("div");
    logEntry.classList.add("transaction-entry", category === "income" ? "income" : "expense");

    logEntry.innerHTML = `
        <strong>${category.toUpperCase()}:</strong> $${amount.toFixed(2)}
        <br><small>${description}</small>
        ${category === "expense" ? `<br><small>Category: ${expenseCategory}</small>` : ""}
    `;

    logEntries.prepend(logEntry);

    // Reset form fields
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "income";
    document.getElementById("expense-category").value = "food";

    // Hide expense category dropdown after reset
    document.getElementById("expense-categories").style.display = "none";
});
