#open('IMO.html', 'x')

a=[
    "IMO",
   "IMOSL",
   "OMCC",
    "OMM",
   "EGMO",
   "OIM",
   "RMM",
   "TSTMX",
   "Algebra",
   "Combinatoria",
   "Geometria",
   "Numeros",
   "Miscelaneo"
   ]
for i in a:
    fp=open("%s.html"%(i),"w")
    htmltext="""
<!DOCTYPE html>


<!-- AAAAAAAAA -->


<html>
    
  <!-- HEAD -->
  <head>
      <!--Example style: <link href="" rel="stylesheet">-->
      <link href="https://fonts.googleapis.com/css?family=Mate" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css?family=Verdana" rel="stylesheet">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
      <link href="/styles/style.css" rel="stylesheet">
      
      <script src="https://code.jquery.com/jquery-1.10.2.js"></script>

      <!-- MathJax Script -->
      <script>
          MathJax = {
              tex: {
                  inlineMath: [['$', '$'], ['\\(', '\\)']]
              }
          };
      </script>
      <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
      
      <meta charset="utf-8">
      <title>Proyecto</title>
  </head>
    
    
    
  <body> 
      <div class="container">

          <!-- PAGE HEADER -->
          <div>
              <div class="row align-items-center">
                  <div class="col-12">
                      <div class="header" id="header-placeholder">

                      </div>
                  </div>
              </div>
              <script>
                  $(function(){
                      $("#header-placeholder").load("header.html");
                  });
              </script>
          </div>

          <!-- PAGE SUBTITLE -->
          <div>
              <div class="row" id="sub-placeholder"> 

              </div>
              <script>
                  $(function(){
                      $("#sub-placeholder").load("subtitle.html");
                  });
              </script>
          </div>

          <!-- PAGE CONTENT -->
          <div id="content", class="row">

              <!-- NAVIGATION MENU -->
              <div class ="col-12 col-md-3 order-md-last pl-md-1" id="nav-placeholder">
                  
              </div>
              <script>
                  $(function(){
                      $("#nav-placeholder").load("nav.html");
                  });
              </script>

              <!-- CONTENT-->
              <div class="col-12 col-md-9 order-md-first pr-md-2">
                  <div id="main">
                      <div class="entry">

                          <h1 id="pagetitle"> 
                              <a href="/index.html">
                               %s <!-- Page Title -->
                              </a>
                          </h1>
                          <div class="entrywrap">

                              <!-- (Begin writing here) -->
                              
                              <!-- (End writing here) -->

                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
      
      <!-- SCRIPTS -->
      <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
      <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  </body>
</html>
"""%(i)
    fp.write(htmltext)
    fp.close



