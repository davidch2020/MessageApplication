document.addEventListener('DOMContentLoaded', () => {

    var rooms = [];

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        const form = document.getElementById('post-message');

        $(".button_id").unbind('click').click(function(){
          var answer = confirm("Are you sure you want to delete this post?");
          if(answer){
            var button_id = this.id;
            console.log(button_id);
            socket.emit('delete', {'button_id': button_id});
            var post = document.getElementById('message' + button_id);
            var delete_button = document.getElementById(button_id);
            var like_button = document.getElementById('post' + button_id);
            var number_of_likes = document.getElementById('likes' + button_id);
            var unlike_button = document.getElementById('unlike' + button_id);
            unlike_button.remove();
            like_button.remove();
            number_of_likes.remove();
            delete_button.remove();
            post.remove();
          }
        });

        $(".like_id").unbind('click').click(function(){
          var like_id = this.id;
          var num_of_likes_id_list = like_id.match(/[a-z]+|[^a-z]+/gi);
          var num_of_likes_id_digit = num_of_likes_id_list[1];
          var num_of_likes_final_id = parseInt(num_of_likes_id_digit, 10);
          var current_num_of_likes = $('#likes' + num_of_likes_final_id).text();
          var current_num_of_likes_final = parseInt(current_num_of_likes, 10);

          current_num_of_likes_final++;
          document.getElementById('likes' + num_of_likes_final_id).innerText = current_num_of_likes_final;

          document.getElementById('unlike' + num_of_likes_final_id).style.visibility = 'visible';
          document.getElementById(like_id).disabled = true;
          console.log(like_id);
          socket.emit('like', {'like_id': like_id});
        });

        $(".unlike_id").unbind('click').click(function() {
          var unlike_id = this.id;
          var unlike_id = unlike_id.match(/[a-z]+|[^a-z]+/gi);
          var unlike_id = unlike_id[1];
          var unlike_id = parseInt(unlike_id, 10);
          var current_num_of_likes_final = $('#likes' + unlike_id).text();
          var current_num_likes_final = parseInt(current_num_of_likes_final, 10);
          current_num_of_likes_final--;
          document.getElementById('likes' + unlike_id).innerText = current_num_of_likes_final;
          document.getElementById('post' + unlike_id).disabled = false;
          document.getElementById('unlike' + unlike_id).style.visibility = "hidden";
          console.log("eliminated");
          socket.emit('unlike', {'unlike_id': unlike_id});
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
        li.setAttribute("id", 'message' + x)
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

        var unlike_btn = document.createElement("BUTTON");
        unlike_btn.innerHTML = "Unlike";
        unlike_btn.setAttribute("id", 'unlike' + x);
        document.querySelector("#post-list").append(unlike_btn);
        document.getElementById('unlike' + x).className += "unlike_id";
        document.getElementById('unlike' + x).style.visibility = 'hidden';

        var num_of_likes = document.createElement("P");
        num_of_likes.innerHTML = "0";
        num_of_likes.setAttribute("id", 'likes' + x);
        document.querySelector('#post-list').append(num_of_likes);

        $(".button_id").unbind('click').click(function(){
          var answer = confirm("Are you sure you want to delete this post?");
          if(answer){
            var button_id = this.id;
            console.log(button_id);
            socket.emit('delete', {'button_id': button_id});
            var post = document.getElementById('message' + button_id);
            var delete_button = document.getElementById(button_id);
            var like_button = document.getElementById('post' + button_id);
            var number_of_likes = document.getElementById('likes' + button_id);
            like_button.remove();
            number_of_likes.remove();
            delete_button.remove();
            post.remove();
          }


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

          document.getElementById('likes' + num_of_likes_final_id).innerText = current_num_of_likes_final;
          document.getElementById('unlike' + num_of_likes_final_id).style.visibility = 'visible';
          document.getElementById(like_id).disabled = true;
          socket.emit('like', {'like_id': like_id});
        });

        $(".unlike_id").unbind('click').click(function() {
          var unlike_id = this.id;
          var unlike_id = unlike_id.match(/[a-z]+|[^a-z]+/gi);
          var unlike_id = unlike_id[1];
          var unlike_id = parseInt(unlike_id, 10);
          var current_num_of_likes_final = $('#likes' + unlike_id).text();
          var current_num_likes_final = parseInt(current_num_of_likes_final, 10);
          current_num_of_likes_final--;
          document.getElementById('likes' + unlike_id).innerText = current_num_of_likes_final;
          document.getElementById('post' + unlike_id).disabled = false;
          document.getElementById('unlike' + unlike_id).style.visibility = "hidden";
          socket.emit('unlike', {'unlike_id': unlike_id});
        });
    });


});
