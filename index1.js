document.addEventListener('DOMContentLoaded', () => {

    var rooms = [];

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        const form = document.getElementById('post-message');

        $(".button_id").click(function(){
          var button_id = this.id;
          console.log(button_id);
          socket.emit('delete', {'button_id': button_id});
        });

        $(".like_id").click(function(){
          var like_id = this.id;
          var num_of_likes_id_list = like_id.match(/[a-z]+|[^a-z]+/gi);
          var num_of_likes_id_digit = num_of_likes_id_list[1];
          var num_of_likes_final_id = parseInt(num_of_likes_id_digit, 10);
          var current_num_of_likes = $('#likes' + num_of_likes_final_id).text();
          var current_num_of_likes_final = parseInt(current_num_of_likes, 10);
          console.log(typeof current_num_of_likes_final);
          current_num_of_likes_final++;
          console.log(current_num_of_likes_final);
          document.getElementById('likes' + num_of_likes_final_id).innerText = current_num_of_likes_final;
          document.getElementById(like_id).disabled = true;
          console.log(like_id);
          socket.emit('like', {'like_id': like_id});
        });

        form.addEventListener('submit', logSubmit);
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
      var room = `${data.room_id}`;
      rooms.push(room);
    });


    socket.on('upload post', data => {
        var x = `${data.length}`;
        x = x - 1
        const li = document.createElement('li');
        li.innerHTML = ` ${data.selection}`;
        document.querySelector('#post-list').append(li);
        var btn = document.createElement("BUTTON");
        btn.setAttribute("id", x);
        btn.innerHTML = "Delete";
        document.querySelector('#post-list').append(btn);
        document.getElementById(x).className += "button_id";

        var like_btn = document.createElement("BUTTON");
        like_btn.innerHTML = "Like";
        like_btn.setAttribute("id", 'post' + x);
        document.querySelector('#post-list').append(like_btn);
        document.getElementById('post' + x).className += "like_id";

        var num_of_likes = document.createElement("P");
        num_of_likes.innerHTML = "0";
        num_of_likes.setAttribute("id", 'likes' + x);
        document.querySelector('#post-list').append(num_of_likes);

        $(".button_id").unbind('click').click(function(){
          var button_id = this.id;
          console.log(button_id);
          socket.emit('delete', {'button_id': button_id});
        });

        $(".like_id").unbind('click').click(function(){
          var like_id = this.id;
          var num_of_likes_id_list = like_id.match(/[a-z]+|[^a-z]+/gi);
          var num_of_likes_id_digit = num_of_likes_id_list[1];
          var num_of_likes_final_id = parseInt(num_of_likes_id_digit, 10);
          var current_num_of_likes = $('#likes' + num_of_likes_final_id).text();
          var current_num_of_likes_final = parseInt(current_num_of_likes, 10);
          console.log(typeof current_num_of_likes_final);
          current_num_of_likes_final++;
          console.log(current_num_of_likes_final);
          document.getElementById('likes' + num_of_likes_final_id).innerText = current_num_of_likes_final;
          document.getElementById(like_id).disabled = true;
          console.log(like_id);
          socket.emit('like', {'like_id': like_id});
        });
    });

});
