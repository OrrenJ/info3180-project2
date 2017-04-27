var app = angular.module("myWishlist", []);

app.controller("addItemCtrl", function($scope, $http){

	var token = $("#auth_token").val();

	$scope.getThumbnails = function(){

		var thumbnail_page_url = $("#thumbnail_page_url").val();
		if(!/^(?:f|ht)tps?\:\/\//.test(thumbnail_page_url)){
			thumbnail_page_url = "http://" + thumbnail_page_url;
		}

		$http({
			method: "GET",
			url: "/api/thumbnails",
			params: {
				url: thumbnail_page_url
			},
			headers: {
				'Authorization': 'Basic ' + token
			}
		}).then(function success(response){
			$scope.response = response.data;
		});
	}

	$scope.select = function(thumbnail){
		$scope.selected = thumbnail;
	}

	$scope.setThumbnail = function(url){
		$("#thumbnail_url").val(url);
	}

	$scope.submit = function(form){

		$http({
			method: "POST",
			url: "/wishlist/add",
			data: $.param({
				csrf_token: $("#csrf_token").val(),
				title: $("#title").val(),
				description: $("#description").val(),
				url: $("#url").val(),
				thumbnail_url: $("#thumbnail_url").val()
			}),
			headers: { 
				'Content-Type': 'application/x-www-form-urlencoded',
				'Authorization': 'Basic ' + token
			}
		}).then(function success(response) {
			var flashes = $(response.data).find("#flashes");
			$("#flashes").html(flashes);
		});
	}

}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('//').endSymbol('//');
});

app.controller("getUsers", function($scope, $http){

	var token = $("#auth_token").val();

	$http({
		method: "POST",
		url: "/api/users",
		headers: {
			'Authorization': 'Basic ' + token
		}
	}).then(function success(response){
		r = response.data
		$scope.users = r.data.users
	});

}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('//').endSymbol('//');
});

app.controller("getUserWishlist", function($scope, $http){

	var token = $("#auth_token").val();
	var userid = $("#user_id").val();

	$http({
		method: "GET",
		url: "/api/users/" + userid + "/wishlist",
		headers: {
			'Authorization': 'Basic ' + token
		}
	}).then(function success(response){
		r = response.data;
		$scope.wishlist = r.data.items;
	});

}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('//').endSymbol('//');
});

app.controller("getMyWishlist", function($scope, $http){

	var token = $("#auth_token").val();
	var userid = $("#user_id").val();

	$http({
		method: "GET",
		url: "/api/users/" + userid + "/wishlist",
		headers: {
			'Authorization': 'Basic ' + token
		}
	}).then(function success(response){
		r = response.data;
		$scope.wishlist = r.data.items;
	});

	$scope.setdelete = function(itemid){
		$scope.todelete = itemid;
	}

	$scope.remove = function(itemid){
		$http({
			method: "DELETE",
			url: '/api/users/' + userid + '/wishlist/' + itemid,
			headers: {
				'Authorization': 'Basic ' + token
			}
		}).then(function success(response){
			location.reload();
		});
		
	}

}).config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('//').endSymbol('//');
});