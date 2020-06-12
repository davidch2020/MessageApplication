document.addEventListener('DOMContentLoaded', () => {

    var rooms = [];

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        const form = document.getElementById('post-message');

        form.addEventListener('submit', logSubmit);
        console.log("Checkpoint");
        function logSubmit(event) {
          const selection = document.getElementById("actual-message").value;
          document.getElementById("actual-message").value = "";
          console.log(selection);
          event.preventDefault();

          if(rooms.length > 0){
            var room = rooms[0];
            console.log(rooms);
            console.log(room);
          }

          socket.emit('recieved post', {'selection': selection, 'room': room});
        }


    });

    socket.on('room_id', data => {
      console.log("Reached here");
      var room = `${data.room_id}`;
      rooms.push(room);
    });



    socket.on('upload post', data => {
        const li = document.createElement('li');
        li.innerHTML = ` ${data.selection}`;
        document.querySelector('#post-list').append(li);
    });
});
