
document.scripts[0].src="/static/js/jtopo-0.4.7-min.js"
/*<script language='javascript' src='/static/js/jtopo-0.4.7-min.js'></script>*/

function build_topo(row_object){
	var url = "/monitor/server_list/?reg={0}"
	reg=row_object['reg']
	var url = url.template(reg)
	//WEB_APP.fontColor = "255.255.255"
    var app="{0}_APP"
	app=app.template(reg)
	var app = node(100, 150, '33.png', reg);
	if (row_object['bad'] > 0) {
		app.alarm = (row_object['bad']);

	}
	app.dbclick(function() {
		//var url = "/monitor/server_list/?reg=WEB"

		window.open(url);
							}
	)
}	
	


	
//<script type='text/javascript'>
	String.prototype.template = function() {
		var args = arguments;
		return this.replace(/\{(\d+)\}/g, function(m, i) {

			return args[i];
		}

		);
	}
//</script>

	
	function node(x, y, img, name) {
		var node = new JTopo.Node(name);
		node.setImage('/static/img/' + img, true);
		node.fontColor = "255.255.0"
		node.setLocation(x, y);
		//scene.add(node);
		return node;
	}
	
	
	

	function hostLink(nodeA, nodeZ) {
		var link = new JTopo.FlexionalLink(nodeA, nodeZ);
		link.shadow = false;
		link.offsetGap = 44;
		scene.add(link);
		return link;
	}