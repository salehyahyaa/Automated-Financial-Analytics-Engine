/**
 * Plaid Link: link token, handler, openPlaidLink for Connect bank account flow.
 * Exposes window.API_BASE and window.openPlaidLink for other scripts.
 */
(function () {
  window.API_BASE = "http://127.0.0.1:5000";
  var plaidHandler = null;
  window.openPlaidLink = function () {
    alert("Cannot open Plaid Link. Make sure the backend is running on port 5000.");
  };

  fetch(window.API_BASE + "/create_link_token")
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(function (data) {
      plaidHandler = Plaid.create({
        token: data.link_token,
        onSuccess: function (public_token, metadata) {
          fetch(window.API_BASE + "/exchange_public_token", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ public_token: public_token })
          })
            .then(function (r) {
              if (!r.ok) throw new Error("HTTP " + r.status);
              return r.json();
            })
            .then(function () {
              return fetch(window.API_BASE + "/sync_checking_accounts", { method: "POST" });
            })
            .then(function () { return fetch(window.API_BASE + "/sync_credit_accounts", { method: "POST" }); })
            .then(function () {
              return fetch(window.API_BASE + "/sync-transactions", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: "{}"
              });
            })
            .then(function () {
              alert("Bank connected! Accounts and transactions synced.");
            })
            .catch(function (err) {
              console.error("Error connecting bank:", err);
              alert("Error connecting bank: " + err.message);
            });
        },
        onExit: function (err, metadata) {
          if (err) console.log("Plaid exit:", err, metadata);
        },
        onError: function (err, metadata) {
          console.error("Plaid error:", err, metadata);
          alert("Plaid error: " + (err.error_message || err.display_message || "Unknown error"));
        }
      });
      window.openPlaidLink = function () {
        if (plaidHandler) plaidHandler.open();
      };
    })
    .catch(function (err) {
      console.error("Error fetching link token:", err);
    });
})();
