package com.example.csrf_lab_java;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
public class FlawedRefererFilter implements Filter {

    private static final String EXPECTED_DOMAIN = "http://localhost:8080";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        
        // A verificação só se aplica a requisições POST para /change-email
        if ("POST".equalsIgnoreCase(httpRequest.getMethod()) && "/change-email".equals(httpRequest.getRequestURI())) {
            String referer = httpRequest.getHeader("Referer");
            System.out.println("[Vulnerável] Recebido Referer: " + referer);

            // LÓGICA FALHA: Aceita se o domínio estiver em QUALQUER LUGAR do Referer
            if (referer == null || !referer.contains(EXPECTED_DOMAIN)) {
                System.out.println("[Vulnerável] Requisição BLOQUEADA");
                HttpServletResponse httpResponse = (HttpServletResponse) response;
                httpResponse.sendError(HttpServletResponse.SC_FORBIDDEN, "Referer inválido!");
                return; // Bloqueia a requisição
            }
            System.out.println("[Vulnerável] Requisição ACEITA");
        }

        chain.doFilter(request, response); // Continua para o próximo filtro ou para o controller
    }
}