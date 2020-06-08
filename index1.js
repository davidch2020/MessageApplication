document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        const form = document.getElementById('post-message');
              // Each button should emit a "submit vote" event
        var room = "abc123"
        form.addEventListener('submit', logSubmit);
        console.log("Checkpoint");
        function logSubmit(event) {
          const selection = document.getElementById("actual-message").value;
          console.log(selection);
          event.preventDefault();
          socket.emit('recieved post', {'selection': selection, 'room': room});
        }


    });

    socket.on('upload post', data => {
        const li = document.createElement('li');
        li.innerHTML = ` ${data.selection}`;
        document.querySelector('#post-list').append(li);
    });
});
