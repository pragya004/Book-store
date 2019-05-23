var app = angular.module("myApp", []);
// communicates with get_users view to show all the users 
app.controller("setup",function($rootScope,$http,$compile){

    var api_url = "http://127.0.0.1:8000/chat/api/fetch/users/";
  
    $http.get(url=api_url).then(function(response){

        var other_users = response.data["user_names"];
        var ul          = document.getElementsByClassName("contacts")[0];

        for(var i = 0 ; i < other_users.length ; i++ )
        {
            var div1 = document.createElement("div");
            var div2 = document.createElement("div");
            var div3 = document.createElement("div");

            div1.className = "container";
            div2.className = "contacts-pic";
            div3.className = "name";

            div3.textContent = other_users[i].username;
            div1.appendChild(div2);
            div1.appendChild(div3);

            div1.setAttribute("ng-click","fetchConversations('" + other_users[i].username + "'," + other_users[i].id + ")");

            $compile(div1)($rootScope);

            ul.appendChild(div1);
        }

    });

});

//fetches convos and messages from restapi and displays them
app.controller("user", function($scope,$rootScope,$http,$interval) {

  var len;

  function fetchMessages(id)
  {    
    $http.get(url="http://127.0.0.1:8000/chat/api/messages?conv_id=" + $scope.conv_id + "&type=1").then(function(response){

       if(len != response.data["messages"].length)
       { 
          var diff = response.data["messages"].length - len;
          len = response.data["messages"].length;
          var messages = response.data["messages"].slice(-diff);

          var ul = document.getElementsByClassName("chat-space")[0];


          for(var i = 0 ; i < messages.length ; i++)
          {
            var div1 = document.createElement("div");
            var p = document.createElement("p");

            p.textContent = messages[i]["message"];
 
            if( response.data["logged_in_user"] == messages[i]["user_id"] )
              div1.className = "sender-text";
            else
              div1.className = "received-text";


            div1.appendChild(p);
            ul.appendChild(div1);

          }

          var objDiv = document.getElementsByClassName("chat-space")[0];

          objDiv.scrollTop = objDiv.scrollHeight;

        }

      });

  }


  $scope.sendMsg = function(){

    if($scope.conv_id != undefined)
    {
      var message = {
        "conversation": $scope.conv_id,
        "type": "1",
        "body": $scope.body,
        
      }

      document.getElementById("name").value = "";
      // console.log(message);

      $http.post(url="http://127.0.0.1:8000/chat/api/messages/",data=message);
  
    }

  }


    function deleteMessages()
    {

        var myNode = document.getElementsByClassName("chat-space")[0];
      
        console.log(myNode);
        
        while (myNode.firstChild)
            myNode.removeChild(myNode.firstChild);
    }


    var stop = null;

    $rootScope.fetchConversations = function(name, id){

        $interval.cancel(stop);

        deleteMessages();

        document.getElementById("selected_user").textContent = name;

        len = 0;

        $http.get("http://127.0.0.1:8000/chat/api/direct/conversation?id=" + id).then(function(response){

        console.log(response.data["conv_id"]);

        $scope.conv_id = response.data["conv_id"];

        var len = 0;

        stop = $interval(fetchMessages, 1000, 0, true, $scope.conv_id);

    });

  }


});
// app.controller("login", function($scope){

// });
