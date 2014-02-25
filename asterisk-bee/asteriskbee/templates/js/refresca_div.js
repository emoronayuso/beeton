
 function ajaxFunction01()
  {
  var xmlHttp;
  try
    {
    // Firefox, Opera 8.0+, Safari
    xmlHttp=new XMLHttpRequest();
    return xmlHttp;
    }
  catch (e)
    {
    // Internet Explorer
    try
      {
      xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
      return xmlHttp;
      }
    catch (e)
      {
      try
        {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
        return xmlHttp;
        }
      catch (e)
        {
        alert("Your browser does not support AJAX!");
        return false;
        }
      }
    }
  }


function fajax1()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
        document.getElementById('div_uso_ram').innerHTML=ajax.responseText;
        }
      }


    ajax.open("get","/admin/status/uso_ram/",true);
    ajax.send(null);
 }




 function fajax2()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
        document.getElementById('div_carga_cpu').innerHTML=ajax.responseText;
        }
      }
   
 
    ajax.open("get","/admin/status/carga_cpu/",true);
    ajax.send(null);    
 } 


function fajax3()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
        document.getElementById('div_uso_sist_raiz').innerHTML=ajax.responseText;
        }
      }


    ajax.open("get","/admin/status/uso_sist_raiz/",true);
    ajax.send(null);
 }


function fajax4()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
        document.getElementById('div_llamadas_activas').innerHTML=ajax.responseText;
        }
      }


    ajax.open("get","/admin/status/llamadas_activas/",true);
    ajax.send(null);
 }


function carga_grafica_cpu()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
          document.getElementById('div_grafica_uso_cpu').innerHTML=ajax.responseText;
        }
      }


    ajax.open("get","/admin/status/genera_grafica_uso_cpu_dia/",true);
    ajax.send(null);
 }


function carga_lista_ext_reg() {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
          document.getElementById('div_lista_ext_reg').innerHTML=ajax.responseText;
        }
      }


    ajax.open("get","/admin/status/lista_ext_reg/",true);
    ajax.send(null);
 }





function carga_api()
 {
    var ajax;
    ajax=ajaxFunction01();
    ajax.onreadystatechange=function()
      {
      if(ajax.readyState==4)
        {
           document.getElementById('div_form_add_linea').innerHTML=ajax.responseText;
          /* document.getElementById('div_add_nueva_linea').innerHTML=ajax.responseText; */
        }
      }

    id_api = document.getElementById('lista_apli').value;
      

    ajax.open("get","/admin/dialplan/mod_contexto/add_linea/?id_api="+id_api+"&add_linea=1",true); 
    ajax.send(null);
 }


function mod_linea_comentada(context,exten,priority){
    var ajax;
    ajax=ajaxFunction01();

    ajax.open("get","/admin/dialplan/mod_contexto/mod_linea_comentada/?context="+context+"&exten="+exten+"&priority="+priority,true);

    ajax.send(null);
 }

function borra_linea(context,exten,priority){
    var ajax;
    ajax=ajaxFunction01();
    
    /*Confirmamos la eliminacion de la linea */
    var statusConfirm = confirm("¿Realmente desea eliminar este linea del contexto "+context+" asociada a la extensión "+exten+"?"); 
 
      if (statusConfirm == true) {

        ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_dialplan_lineas_contexto').innerHTML=ajax.responseText;
          }
        }

 
      ajax.open("get","/admin/dialplan/mod_contexto/borra_linea/?context="+context+"&exten="+exten+"&priority="+priority,true); 
       
      ajax.send(null);
   
      } 



 }


function borra_audio(id_audio){
    var ajax;
    ajax=ajaxFunction01();

    /*Confirmamos la eliminacion del audio seleccionado */
    var statusConfirm = confirm("¿Realmente desea eliminar este fichero de audio?");

    if (statusConfirm == true) {

        ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_lista_fich_audio').innerHTML=ajax.responseText;
          }
        }
 
     

      ajax.open("get","/admin/admin_audio/borra_audio/?id_audio="+id_audio,true);

      ajax.send(null);
    }
}



function borra_audio_moh(name_audio){
    var ajax;
    ajax=ajaxFunction01();

    /*Confirmamos la eliminacion del audio seleccionado */
    var statusConfirm = confirm("¿Realmente desea eliminar este fichero de audio "+name_audio+" de música en espera?");

    if (statusConfirm == true) {

        ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_lista_moh').innerHTML=ajax.responseText;
          }
        }



      ajax.open("get","/admin/moh/borra_moh/?name_audio="+name_audio,true);

      ajax.send(null);
    }
}



function envia_form(){
 //alert("weee");
  var statusConfirm = confirm("Se va a generar el informe de llamadas en pdf... \nEsta operacion puede tardar unos minutos dependiendo del numero de registros");

 if (statusConfirm == true) {
      document.getElementById('genera_pdf').value=1;
      document.getElementById("form_busqueda_cdr").submit();
 }

}


function borra_sip(id,callerid){
    var ajax;
    ajax=ajaxFunction01();

    /*Confirmamos la eliminacion de la extension sip */
    var statusConfirm = confirm("¿Realmente desea eliminar la extension con callerid: "+callerid+"?");

      if (statusConfirm == true) {

        ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_extensiones_sip_lista').innerHTML=ajax.responseText;
           }
       }


      ajax.open("get","/admin/sip/del_sip/?id="+id,true);

      ajax.send(null);

     }

 }


function borra_iax(name,callerid){
    var ajax;
    ajax=ajaxFunction01();

    /*Confirmamos la eliminacion de la extension sip */
    var statusConfirm = confirm("¿Realmente desea eliminar la extension con callerid: "+callerid+"?");

      if (statusConfirm == true) {

        ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_extensiones_iax_lista').innerHTML=ajax.responseText;
           }
       }


      ajax.open("get","/admin/iax/del_iax/?name="+name,true);

      ajax.send(null);

     }

 }





 function carga_historial(e){
  
    if(window.event)keyCode=window.event.keyCode;
    else if(e) keyCode=e.which;

    var ajax;
    ajax=ajaxFunction01();

      //tecla arriba
    if (keyCode == 38){
       
        ajax.onreadystatechange=function(){
           if(ajax.readyState==4){
              document.getElementById('div_input_comando').innerHTML=ajax.responseText;
            }
         }
     
        id = parseInt(document.getElementById('id_historial_comando').value) + 1;
 
        if ( parseInt(document.getElementById('id_tam_historial').value)<id ){
           id = parseInt(document.getElementById('id_tam_historial').value);
        }else{
          id = parseInt(document.getElementById('id_historial_comando').value) + 1;
        }
  
         document.getElementById('id_historial_comando').value = id;

         ajax.open("get","/admin/consola/historial_consola/?id_historial_comando="+id,true);

         ajax.send(null);
       

     //tecla abajo
    }else if(keyCode == 40){
    
         ajax.onreadystatechange=function(){
           if(ajax.readyState==4){
              document.getElementById('div_input_comando').innerHTML=ajax.responseText;
            }
         }

        if (parseInt(document.getElementById('id_historial_comando').value)>1 ){

          id = parseInt(document.getElementById('id_historial_comando').value) - 1;
        }else{
          id=1;
        }
    
          document.getElementById('id_historial_comando').value = id;


        ajax.open("get","/admin/consola/historial_consola/?id_historial_comando="+id,true);

        ajax.send(null);
 
    }
   
       //Si el navegador no soporta la propiedad autofocus de input
  if( !("autofocus" in document.createElement("input")) ){
       document.getElementById("id_comando").focus();
   }

 
 }//Fin funcion carga_historial


function carga_consola() {

 //Ponemor el foco en el input_comando.
 document.getElementById("id_comando").focus();

 //Ponemos el scrollbar del div_consola abajo 
 var div_scroll = document.getElementById('div_consola');
 div_scroll.scrollTop = div_scroll.scrollHeight + div_scroll.offsetHeight;

}


function sele_linea(id_linea_sele,id_div_sele) {
   
   //Antes de guardar la nueva linea seleccionada ponemos el color del div seleccionado actual 
     var div_anterior = document.getElementById(document.getElementById('input_id_div_sele').value);
    
     if (div_anterior != null){
        div_anterior.style.backgroundColor = document.getElementById('input_color_linea_sele').value;
     }


      document.getElementById('input_color_linea_sele').value = document.getElementById(id_div_sele).style.backgroundColor;
      
      document.getElementById('input_id_div_sele').value = id_div_sele;     

      document.getElementById(id_div_sele).style.backgroundColor = 'blue';
 
      document.getElementById('input_id_linea_sele').value = id_linea_sele;
   
}


function cambia_linea(opcion) {

 
 if(document.getElementById('input_id_div_sele').value == ""){
    alert("Debe seleccionar antes una linea del dialplan");
  }else{

     var ajax;
     ajax=ajaxFunction01();

      ajax.onreadystatechange=function(){
          if(ajax.readyState==4){
             document.getElementById('div_dialplan_lineas_contexto').innerHTML=ajax.responseText;
          }
        }//Fin funcion ajax
 
      id_linea_sele = document.getElementById('input_id_linea_sele').value;
      div_linea = document.getElementById('input_id_div_sele').value;
      context = div_linea.split('_')[2];      

      ajax.open("get","/admin/dialplan/mod_contexto/cambia_linea/?context="+context+"&id_linea_sele="+id_linea_sele+"&"+opcion+"=1",true);

      ajax.send(null);


 }

}//Fin funcion cambia_linea


function shutdown() {
 // alert("apagarrrr")

  /*Confirmamos el apagado de la PBX */
    var statusConfirm = confirm("¿Realmente quiere APAGAR LA PBX?");

      if (statusConfirm == true) {

          var ajax;
          ajax=ajaxFunction01();

          ajax.open("get","/admin/status/shutdown/",true);

          ajax.send(null);
     }
}//Fin shutdown

function muestra_oculta_opc_a_ext(tipo_ext) {

 /* Cambiamos la imagen del desplegable   */
  var imagen_des = document.getElementById('id_imagen_des_opc_a');

   parte_url = location.href.split('?');

   imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;

 
 id_div = "div_contenedor_opc_a_"+tipo_ext;

 var div_sele = document.getElementById(id_div);
 div_sele.style.display = (div_sele.style.display == 'block') ? 'none' : 'block';


}



function borra_app(nombre_app) {
   alert("Esta funcion aún no esta implementada!");
}



/*Incluimos los fichero javascript de las api instaladas */
document.write("<script src = '/js/ivr.js' language = 'JavaScript' type = 'text/javascript'></script>");
/* document.write("<script src = '/js/moh.js' language = 'JavaScript' type = 'text/javascript'></script>"); */
document.write("<script src = '/js/moh.js' language = 'JavaScript' type = 'text/javascript'></script>");
