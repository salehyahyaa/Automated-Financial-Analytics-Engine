/**
 * Chat UI: dropdown (Connect bank), send message, textarea behavior, panel resize.
 * Uses window.openPlaidLink from plaid.js.
 */
(function () {
  function initChatModeDropdown() {
    var trigger = document.getElementById("chat-extra-btn");
    var dropdown = document.getElementById("chat-mode-dropdown");
    if (!trigger || !dropdown) return;

    function closeDropdown() {
      dropdown.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
      document.removeEventListener("click", onDocumentClick);
    }

    function onDocumentClick(e) {
      if (!dropdown.contains(e.target) && !trigger.contains(e.target)) closeDropdown();
    }

    trigger.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = dropdown.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", isOpen ? "true" : "false");
      if (isOpen) {
        requestAnimationFrame(function () {
          document.addEventListener("click", onDocumentClick);
        });
      } else {
        document.removeEventListener("click", onDocumentClick);
      }
    });

    dropdown.querySelectorAll(".chat-mode-dropdown-item").forEach(function (item) {
      item.addEventListener("click", function (e) {
        e.stopPropagation();
        closeDropdown();
        if (item.getAttribute("data-action") === "connect-bank" && window.openPlaidLink) window.openPlaidLink();
      });
    });
  }

  var chatMessages = document.getElementById("chat-messages");
  var chatInput = document.getElementById("chat-input");
  var chatSend = document.getElementById("chat-send");


  function appendMessage(role, text) {
    var wrap = document.createElement("div");
    wrap.className = "chat-message " + (role === "user" ? "chat-message-user" : "chat-message-assistant");
    var bubble = document.createElement("div");
    bubble.className = "chat-message-bubble";
    var p = document.createElement("p");
    p.textContent = text;
    bubble.appendChild(p);
    wrap.appendChild(bubble);
    chatMessages.appendChild(wrap);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }


  function sendMessage() {
    var text = (chatInput.value || "").trim();
    if (!text) return;
    chatInput.value = "";
    appendMessage("user", text);
    appendMessage("assistant", "Reply from the assistant will go here. Connect a backend chat endpoint to respond.");
  }

  if (chatSend) chatSend.addEventListener("click", sendMessage);
  if (chatInput) {
    chatInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    chatInput.addEventListener("input", function () {
      this.style.height = "auto";
      this.style.height = Math.min(this.scrollHeight, 140) + "px";
    });
  }


  function initChatResize() {
    var column = document.getElementById("chat-column");
    var handle = document.getElementById("chat-resize-handle");
    if (!column || !handle) return;
    var minW = 320;
    var maxW = 720;
    var startX = 0;
    var startW = 0;


    function onMouseMove(e) {
      var dx = startX - e.clientX;
      var newW = Math.min(maxW, Math.max(minW, startW + dx));
      column.style.width = newW + "px";
    }
    
    
    function onMouseUp() {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    }
    handle.addEventListener("mousedown", function (e) {
      e.preventDefault();
      startX = e.clientX;
      startW = column.offsetWidth;
      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
    });
  }

  initChatModeDropdown();
  initChatResize();
})();
