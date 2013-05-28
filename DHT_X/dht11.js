
	function TempHumidity(name) {
		this.name = name;
		this.url = "/devices/" + name + "/sensor";
		this.refreshTime = 1000;
	}

	TempHumidity.prototype.toString = function() {
		return "";
	}

	TempHumidity.prototype.getCelsius = function(callback) {
		$.get(this.url + "/temperature/c", function(data) {
			callback(this.name, data);
		});
	}

	TempHumidity.prototype.getPercent = function(callback) {
		$.get(this.url + "/humidity", function(data) {
			callback(this.name, data);
		});
	}

	TempHumidity.prototype.refreshUI = function() {
		var temp = this;
		var element = this.element;
		if (element != undefined)
			if (element.header1 == undefined) {
				element.header1 = $("<h3>" + this + "</h3>");
				element.append(element.header1);
			}
			if (element.header2 == undefined) {
				element.header2 = $("<h3>" + this + "</h3>");
				element.append(element.header2);
			}
		
		this.refreshTemp();
		this.refreshPercent();
	}

	TempHumidity.prototype.refreshTemp = function(){
		var temp = this;
		var element = this.element;
		this.getCelsius(function(name, data){
			if (element != undefined) {
				element.header1.text(temp + data + "°C");
			}
			setTimeout(function(){temp.refreshTemp()}, temp.refreshTime);
		});
	}

	TempHumidity.prototype.refreshPercent = function(){	
		var temp = this;
		var element = this.element;
		this.getPercent(function(name, data){
			if (element != undefined) {
				element.header2.text(temp + data + "%");
			}
			setTimeout(function(){temp.refreshPercent()}, temp.refreshTime);
		});
	}