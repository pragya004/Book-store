var app = angular.module("myApp", []);
app.controller("setup",function($rootScope,$http,$compile){


    var api_url = "http://127.0.0.1:8000/chat/api/fetch/groups/";
  
    $http.get(url=api_url).then(function(response){

        var groups = response.data["group_details"];
        var ul     = document.getElementById("groups-list");

        for(var i = 0 ; i < groups.length ; i++ )
        {
            var div1 = document.createElement("div");
            var div3 = document.createElement("div");

            div1.className = "container";
            div3.className = "group-name";

            div3.textContent = groups[i].name;
            div1.appendChild(div3);

            div1.setAttribute("ng-click","fetchConversations('" + groups[i].name + "'," + 
                                                            "'" + groups[i].description + "'," + groups[i].id + ")");
            $compile(div1)($rootScope);
            ul.appendChild(div1);
        }

    });

});


app.controller("user", function($scope,$rootScope,$http,$interval) {
  
    var len;

    function fetchMessages(id)
    {    
        $http.get(url="http://127.0.0.1:8000/chat/api/messages?conv_id=" + $scope.conv_id + "&type=2")
        .then(function(response){

            if(len != response.data["messages"].length)
            { 
                var diff = response.data["messages"]
                .length - len;
                len = response.data["messages"].length;
                var messages = response.data["messages"].slice(-diff);

                var ul = document.getElementById("chat-space");


                for(var i = 0 ; i < messages.length ; i++)
                {
                    var div1 = document.createElement("div");
                    var p = document.createElement("p");

                    p.textContent = messages[i].user_name + " : " + messages[i]["message"];
     
                    if( response.data["logged_in_user"] == messages[i]["user_id"] )
                        div1.className = "sender-text";
                    else
                        div1.className = "received-text";


                    div1.appendChild(p);
                    ul.appendChild(div1);

                }

                var objDiv = document.getElementById("chat-space");

                objDiv.scrollTop = objDiv.scrollHeight;

            }

        });

    }


    $scope.sendMsg = function(){

        if($scope.conv_id != undefined)
        {
            var message = { "conversation": $scope.conv_id,
                            "type": "2",
                            "body": $scope.body}


            document.getElementById("name").value = "";

            $http.post(url="http://127.0.0.1:8000/chat/api/messages/",data=message);
        }
    }


    function deleteMessages()
    {
        var myNode = document.getElementById("chat-space");

        while (myNode.firstChild)
            myNode.removeChild(myNode.firstChild);
    }

    var stop = null;

    $rootScope.fetchConversations = function(name, description, id){

        $interval.cancel(stop);
        deleteMessages();
        
        document.getElementById("selected_group").textContent = name;
        document.getElementById("group_description").textContent = description;
        
        len = 0;

        $http.get("http://127.0.0.1:8000/chat/api/group/adduser?id=" + id).then(function(response){

            $scope.conv_id = id;

            var len = 0;

            stop = $interval(fetchMessages, 1000, 0, true, $scope.conv_id);

        });

    }


});



  

// app.controller("login", function($scope){

// });
