$(document).ready(function() {
       // executes when HTML-Document is loaded and DOM is ready
      console.log("document is ready");
        

        $( ".card" ).hover(
        function() {
          $(this).addClass('shadow-lg').css('cursor', 'pointer');
          // $(this).addClass('mt-2').css('cursor', 'pointer');
        }, function() {
          $(this).removeClass('shadow-lg');
          // $(this).removeClass('mt-2');
        }
      );
  
      // document ready  
      });
