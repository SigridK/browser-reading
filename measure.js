var webPage = require('webpage');
var fs = require('fs');

var system = require('system')
// 'file:///users/anders/Downloads/pagedump/sentence.html'
if (system.args.length != 3) {
    console.log('Usage: measure.js URL filename');
    phantom.exit(1);
}

var inputUrl = system.args[1]
// Prefix of outputFile - not in URL syntax
var outputFile = system.args[2]

var page = webPage.create();
page.viewportSize = { width: 1280, height: 1024 };
//page.paperSize = { width: '1024px', height: '768px', margin: '0px' }

page.open(inputUrl, function(status) {
  var boxes  = page.evaluate(function() {
  	var info = Array()
  	var children = document.getElementsByClassName("char");
  	for (var i = 0; i < children.length; i++) {
  		var child = children[i];
  		var bb = child.getBoundingClientRect()
  		info.push({text: child.textContent,
  				   id: child.getAttribute("id"),
  				   bottom: bb.bottom,
  				   height: bb.height,
  				   left: bb.left,
  				   right: bb.right,
  				   top: bb.top,
  				   width: bb.width})
  	}
    
    return info;
  });

	var stream = fs.open(outputFile+".tsv", 'w');
	var columns = ['id', 'text', 'height', 'width', 'top', 'bottom', 'left', 'right']
	stream.write(columns.join("\t"))
	stream.write("\n")
	for (var i in boxes) {
		var box = boxes[i]
		var line = [box.id, box.text, box.height, box.width, box.top, box.bottom, box.left, box.right]		
		stream.write(line.join("\t"))
		stream.write("\n")
  		// console.log(boxes[i].text, boxes[i].left);
	}
	stream.close()

  page.render(outputFile+".png")

  phantom.exit();
});
