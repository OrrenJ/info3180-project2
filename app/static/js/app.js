var app = angular.module("myWishlist", []);

app.controller("addItemCtrl", function($scope, $http){

	var userid = $("#userid").val();
	var token = $("#auth_token").val();

	$http.defaults.headers.common['Authorization'] = 'Basic ' + token;

	$scope.thumbnails = {};
	$scope.thumbnail_chosen = false;

	$scope.addItem = function(){

		$http({
	        method: "POST",
	        url: "/api/users/" + userid + "/wishlist",
	        data: $.param({
	        	title: $("#title").val(),
	        	description: $("#description").val(),
	        	url: $("#url").val(),
	        	thumbnail_url: $("#thumbnail_url").val()
	        }),
	        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
	    }).then(function success(response){
	    	console.log(response.data);
	        $scope.response = response.data;
	    });
	};

	$scope.pickImage = function(){

		$("#fetching-thumbnails").show();

		$http({
			method: "GET",
			url: "/api/thumbnails",
			params: { 
				url: $("#thumbnail_page_url").val()
			}
		}).then(function success(response){
			$("#fetching-thumbnails").hide();
			console.log(response.data);
			$scope.response = response.data;
			$scope.thumbnails = $scope.response.data.thumbnails;
		});
	}

	$scope.imageChoice = function(url){



	}

}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('//').endSymbol('//');
});