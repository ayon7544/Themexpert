const importantNoticeTable = document.getElementById('important-notice-for-honours-table');

// Establish a WebSocket connection to the server.
const socket = new WebSocket('ws://localhost:8000/important-notice-data');

// Listen for messages from the server.
socket.onmessage = function(event) {
  // Parse the important notice data.
  const importantNoticeData = JSON.parse(event.data);

  // Populate the important notice table.
  importantNoticeTable.innerHTML = '';
  for (const notice of importantNoticeData) {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${notice.sl}</td>
      <td>${notice.title}</td>
      <td>${notice.publishDate}</td>
      <td><a href="${notice.downloadUrl}">Download</a></td>
    `;
    importantNoticeTable.appendChild(row);
  }
};

// Send a ping message to the server every 10 seconds.
setInterval(function() {
  socket.send('ping');
}, 10000);