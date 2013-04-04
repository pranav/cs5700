#/bin/sh

#JAVA=kaffe
JAVA=gij-3.3
CLASSPATH=classes:/usr/share/java/gtk.jar:/usr/share/java/gnome.jar
MAINCLASS=org.klomp.snark.SnarkGnome

${JAVA} -classpath ${CLASSPATH} ${MAINCLASS} $*
