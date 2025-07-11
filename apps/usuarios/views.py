from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Depoimento
from .forms import ContatoForm
from django.utils.safestring import mark_safe


def depoimentos(request):
    """Página de depoimentos"""
    depoimentos_list = Depoimento.objects.filter(ativo=True)
    
    context = {
        'depoimentos': depoimentos_list,
    }
    return render(request, 'usuarios/depoimentos.html', context)


def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            contato_obj = form.save()
            try:
                assunto = f"[New Life] {contato_obj.assunto}"
                mensagem = f"""
Nova mensagem recebida:

Nome: {contato_obj.nome}
Email: {contato_obj.email}
Assunto: {contato_obj.assunto}

Mensagem:
{contato_obj.mensagem}

Enviado via site New Life.
                """

                send_mail(
                    subject=assunto,
                    message=mensagem,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )

                messages.success(request, 'Mensagem enviada com sucesso!')
            except Exception as e:
                import traceback
                print("ERRO AO ENVIAR E-MAIL:\n", traceback.format_exc())

                erro_html = f"""
                <strong>Erro ao enviar email:</strong><br>
                Tipo: {type(e).__name__}<br>
                Detalhe: {str(e)}
                """
                messages.error(request, mark_safe(erro_html))
        else:
            erros = []
            for campo, lista in form.errors.items():
                for erro in lista:
                    erros.append(f"<strong>{campo}:</strong> {erro}")
            mensagens_html = "Formulário inválido:<br>" + "<br>".join(erros)
            messages.error(request, mark_safe(mensagens_html))
    else:
        form = ContatoForm()

    return render(request, 'usuarios/contato.html', {'form': form})





