function muestra_oculta_div_moh(id_sele_moh,id_div,id_param,id_des_param,lista_opciones,id_imagen_des) {

      sele = document.getElementById(id_sele_moh);


    /*Cambiamos la imagen del desplegable  y visualizamos el bloque si ya esta inicializado*/
      var imagen_des = document.getElementById(id_imagen_des);

     parte_url = location.href.split('?');

     imagen_des.src = (imagen_des.src == parte_url[0]+'images/desplegable_mas.png') ? parte_url[0]+'images/desplegable_menos.png' : parte_url[0]+'images/desplegable_mas.png' ;




      if (sele.length == 0) {
       for (i=0; i<lista_opciones.length; i++){

           sele.options.add(new Option(lista_opciones[i], lista_opciones[i]) );

           if(document.getElementById(id_param).value == lista_opciones[i] ){
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




function selecciona_moh(id_sele_moh,id_param_moh) {

   sele = document.getElementById(id_sele_moh);

   document.getElementById(id_param_moh).value = sele.options[sele.selectedIndex].value

}

