function carga_dias_semana(id_div,id_des_param,id_sele_dia_de,id_sele_dia_a,id_param,id_imagen) {

     var div_sele = document.getElementById(id_div);
     div_sele.style.display = (div_sele.style.display == 'block') ? 'none' : 'block';

     var  div_sele_des = document.getElementById(id_des_param);
     div_sele_des.style.display = (div_sele_des.style.display == 'block') ? 'none' : 'block';

 
    if(document.getElementById(id_param).value == ""){
      document.getElementById(id_param).value = "Lunes-Lunes";
    }else{
       parte_param_dias = document.getElementById(id_param).value.split('-');
 
       array_sele_de = document.getElementById(id_sele_dia_de).options;       
       array_sele_a  = document.getElementById(id_sele_dia_a).options;	

  
       for(i=0; i<array_sele_de.length; i++){
          if(array_sele_de[i].value == parte_param_dias[0]){
            //alert(array_sele_de[i].value + " -- " + array_sele_a[i].value);
             array_sele_de[i].selected = true;
           }
           if(array_sele_a[i].value == parte_param_dias[1]){
             array_sele_a[i].selected = true;
           }
        }
  
    } 



     var imagen_des = document.getElementById(id_imagen);

     parte_url = location.href.split('?');

     imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;


}





function anade_dia(id_sele_dia,id_param){
   
   parte_sele_dia = id_sele_dia.split('_');
   parte_param_dias = document.getElementById(id_param).value.split('-');

   if(parte_sele_dia[2] == "de"){       
     document.getElementById(id_param).value = document.getElementById(id_sele_dia).value +"-"+ parte_param_dias[1];
   }else{
     document.getElementById(id_param).value = parte_param_dias[0] +"-"+document.getElementById(id_sele_dia).value
   }

}






function carga_hora(id_div,id_des_param,id_param,id_hora_de,id_hora_a,id_imagen) {

     
    /* Cambiamos la opcion display del css para que muestre o no el parametro y su descripcion */

     var div_sele = document.getElementById(id_div);
     div_sele.style.display = (div_sele.style.display == 'block') ? 'none' : 'block';

     var  div_sele_des = document.getElementById(id_des_param);
     div_sele_des.style.display = (div_sele_des.style.display == 'block') ? 'none' : 'block';
    



    if(document.getElementById(id_param).value != ""){
         
        int_hora = document.getElementById(id_param).value.split('-');
        document.getElementById(id_hora_de).value = int_hora[0];
        document.getElementById(id_hora_a).value = int_hora[1];


     }

   


     var imagen_des = document.getElementById(id_imagen);

     parte_url = location.href.split('?');

     imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;
  

}



function anade_hora(id_param,id_parte_hora) {

  p = id_parte_hora.split("_");

  valor_actual_hora = document.getElementById(id_param).value;

  if(p[1]== "a"){

      ho = valor_actual_hora.split('-');
      
      document.getElementById(id_param).value = ho[0] +"-"+ document.getElementById(id_parte_hora).value;

   }else{

      if(p[1]== "de"){

        ho = valor_actual_hora.split('-');

        document.getElementById(id_param).value = document.getElementById(id_parte_hora).value +"-"+ ho[1];


      }

   }
   


}







function muestra_oculta_div_audio(id_sele_audio_ivr,id_div,id_param,id_des_param,lista_opciones,lista_valores,id_imagen_des) {
 
      sele = document.getElementById(id_sele_audio_ivr);


    /*Cambiamos la imagen del desplegable  y visualizamos el bloque si ya esta inicializado*/
      var imagen_des = document.getElementById(id_imagen_des);

     parte_url = location.href.split('?');
 
     imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;




   if (sele.length == 0) { 
       for (i=0; i<lista_valores.length; i++){ 
      
           sele.options.add(new Option(lista_opciones[i], lista_valores[i]) );
       
           if(document.getElementById(id_param).value == lista_valores[i] ){
             sele.selectedIndex=i;
           }             
            

        }
     }

     /* Cambiamos la opcion display del css para que muestre o no el parametro y su descripcion */
     var div_sele = document.getElementById(id_div);
     div_sele.style.display = (div_sele.style.display == 'block') ? 'none' : 'block';

     var  div_sele_des = document.getElementById(id_des_param);
     div_sele_des.style.display = (div_sele_des.style.display == 'block') ? 'none' : 'block';

}





function selecciona_audio(id_sele_audio_ivr,id_param_audio) {

   sele = document.getElementById(id_sele_audio_ivr);

   document.getElementById(id_param_audio).value = sele.options[sele.selectedIndex].value

}





/////////////////////////////////////////////////////////////////////////////////////////////////


function muestra_oculta_div_opc_ivr() {
 
     /* Cambiamos la imagen del desplegable si la tabla esta inicializada */
        tabla = document.getElementById('tabla_opciones_ivr');
  
           var imagen_des = document.getElementById('id_imagen_des_8');

           parte_url = location.href.split('?');

           imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;



 
 
    borra_tabla('tabla_opciones_ivr');

    muestra_param('param8_ivr');  
 
     var div_sele = document.getElementById("param8_ivr");
     div_sele.style.display = (div_sele.style.display == 'block') ? 'none' : 'block'; 


 
}


function borra_tabla(id_tabla) {
    
      var elmtTable = document.getElementById(id_tabla);
      var tableRows = elmtTable.getElementsByTagName('tr');
      var rowCount = tableRows.length;

      for (var x=2; x<rowCount; x++) {
        tableRows[x].innerHTML="";
      }

}//Fin funcion borra_tabla


function muestra_param(id_div) {

    /*FORMATO de string_opciones: "1-[contexto_opcion_1]/[extension_opcion_1]/[prioridad_opcion_1],2-.....,"  */

       string_opciones = document.getElementById("id_param8").value;


       opciones = new Array();
       opciones = string_opciones.split(',');

       opcion1 = new Array();   
       opcion2 = new Array();

          for(i=0;i<opciones.length-1;i++){
             opcion1 = opciones[i].split('-');
             /* opcion1[0] contiene al numero */
    
             opcion2 = opcion1[1].split('/');
          
             /* opcion2[0] contiene el contexto */
             /* opcion2[1] contiene la extension */
             /* opcion2[2] contiene la prioridad */

            /* Generamos la tabla con las opciones del IVR */

            var tbody = document.getElementById("tabla_opciones_ivr").getElementsByTagName("tbody")[0];

            var row = document.createElement("tr")

            var td1 = document.createElement("td")
            td1.appendChild(document.createTextNode("columna 1"))
            var td2 = document.createElement("td")
            td2.appendChild(document.createTextNode("columna 2"))
            var td3 = document.createElement("td")
            td3.appendChild (document.createTextNode("columna 3"))
            var td4 = document.createElement("td")
            td4.appendChild (document.createTextNode("columna 4"))


            row.appendChild(td1).innerHTML=opcion1[0];
            row.appendChild(td2).innerHTML=opcion2[0];
            row.appendChild(td3).innerHTML=opcion2[1];
            row.appendChild(td4).innerHTML=opcion2[2];

            tbody.appendChild(row);         
         
         }//Fin Para


    //   muestra_oculta_div(id_div);

}//Fin funcion


function num_opciones(string_opciones){
   var num = 0;
   
   opciones = new Array();
   opciones = document.getElementById("id_param8").value.split(',');

   num = opciones.length;

  return num;
}


function anade_opcion_ivr(string_opciones){

   num_ele = document.getElementById("num_opc_ivr").value;
   index_context_ele = document.getElementById("sele_contexto_ivr").options.selectedIndex;
   context_ele = document.getElementById("sele_contexto_ivr").options[index_context_ele].text;
   exten_ele = document.getElementById("exten_opc_ivr").value;
   prio_ele = document.getElementById("prio_opc_ivr").value;

   if(exten_ele != "" && prio_ele !=""){ 

     document.getElementById("id_param8").value = document.getElementById("id_param8").value + num_ele+"-"+context_ele+"/"+exten_ele+"/"+prio_ele+","; 

     borra_tabla('tabla_opciones_ivr');

     document.getElementById("num_opc_ivr").value = parseInt(document.getElementById("num_opc_ivr").value)+1;

      muestra_param('param8_ivr');

   }

}






