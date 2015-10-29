#/bin/sh

MINIFICATION=0

js[0]="forum/skins/default/media/js/osqa.main.js"
js[1]="forum/skins/default/media/js/jquery.caret.js"
js[2]="forum/skins/default/media/js/osqa.ask.js"
js[3]="forum/skins/default/media/js/osqa.question.js"
js[4]="forum/skins/default/media/js/iframeit.js"

js_min="forum/skins/default/media/js/osqa.main.min.js"

for i in "${js[@]}"
do
   :
   # do whatever on $i
	if [ "$js_min" -ot "$i" ]; then
		cat ${js[@]} > "/tmp/osqa.js"  
		yui-compressor "/tmp/osqa.js" -o "$js_min"
		echo "Javascript changed, commit minified file!"
		MINIFICATION=1
		break		
	fi
done

css[0]="forum/skins/default/media/style/jquery.autocomplete.css"
css[1]="forum/skins/default/media/style/style.css"
css[2]="forum/skins/default/media/style/user.css"
css[3]="forum/skins/default/media/style/auth.css"

css_min="forum/skins/default/media/style/style.min.css"

for i in "${css[@]}"
do
   :
   # do whatever on $i
	if [ "$css_min" -ot "$i" ]; then
		cat ${css[@]} > "/tmp/osqa.css"  
		java  -Xss2048k -jar "/usr/share/yui-compressor/yui-compressor.jar" "/tmp/osqa.css" -o "$css_min"
		echo "CSS changed, commit minified file!"
		MINIFICATION=1
		break		
	fi
done

if [ $MINIFICATION -ne 0 ]; then
	exit 1
fi
exit 0
