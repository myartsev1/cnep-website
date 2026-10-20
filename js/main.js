(function(){
  var btn=document.querySelector('.menu-btn'),nav=document.querySelector('.mobile-nav');
  if(btn&&nav){btn.addEventListener('click',function(){var o=nav.classList.toggle('is-open');btn.setAttribute('aria-expanded',o?'true':'false');});}
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
  } else {document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in');});}

  /* Inquiry form: POST to the configured endpoint (e.g. Formspree) and show a confirmation.
     If no endpoint is configured, compose the message in the visitor's mail app instead. */
  document.querySelectorAll('.iform').forEach(function(form){
    var status=form.querySelector('.iform__status');
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      if(!form.checkValidity()){form.reportValidity();return;}
      var f=new FormData(form),d={};f.forEach(function(v,k){d[k]=v;});
      if(d._gotcha){return;}
      var endpoint=form.getAttribute('data-endpoint');
      if(endpoint){
        status.textContent='Sending…';
        fetch(endpoint,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/json'},
          body:JSON.stringify({name:d.name,email:d.email,affiliation:d.affiliation,topic:d.topic,message:d.message,_replyto:d.email,_subject:'CNEP inquiry: '+d.topic})})
        .then(function(r){if(!r.ok)throw new Error(r.status);form.classList.add('is-sent');status.textContent='Thank you. Your message has been sent and we will be in touch.';form.reset();})
        .catch(function(){status.textContent='Something went wrong. Please try again in a moment.';});
      } else {
        var to=form.getAttribute('data-to');
        var body='Name: '+d.name+'\nEmail: '+d.email+(d.affiliation?'\nAffiliation: '+d.affiliation:'')+'\n\n'+d.message;
        window.location.href='mailto:'+to+'?subject='+encodeURIComponent('CNEP inquiry: '+d.topic)+'&body='+encodeURIComponent(body);
        status.textContent='Opening your email app to send this message.';
      }
    });
  });
})();
