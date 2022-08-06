if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
settings.inlinetex=true;
deletepreamble();
defaultfilename="compilacion-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);


size(45, 45);
unitsize(0.5 cm);
draw((0,0)--(1,0));
draw((0,1)--(1,1));
draw((2,1)--(3,1));
draw((0,2)--(3,2));
draw((0,3)--(3,3));
draw((0,0)--(0,3));
draw((1,0)--(1,3));
draw((2,1)--(2,3));
draw((3,1)--(3,3));
size(45.0pt,0,keepAspect=true);
