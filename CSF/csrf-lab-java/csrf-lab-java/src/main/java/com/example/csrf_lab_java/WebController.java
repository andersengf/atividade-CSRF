package com.example.csrf_lab_java;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.security.Principal; // Import necessário
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Controller
public class WebController {

    // Simulação de um banco de dados de usuários
    private static final Map<String, String> userEmails = new ConcurrentHashMap<>();

    static {
        userEmails.put("wiener", "wiener@exemplo.com");
    }

    @GetMapping("/")
    public String home(Model model, Principal principal) { // MUDANÇA AQUI
        if (principal == null) {
            return "redirect:/login";
        }
        // Pega o nome do usuário diretamente do objeto de segurança 'Principal'
        String username = principal.getName(); // MUDANÇA AQUI

        model.addAttribute("username", username);
        model.addAttribute("email", userEmails.get(username));
        return "home";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

    // O método loginSuccessHandler foi REMOVIDO por ser desnecessário

    @PostMapping("/change-email")
    public String changeEmail(@RequestParam String email, Principal principal) { // MUDANÇA AQUI
        if (principal == null) {
            return "redirect:/login";
        }
        // Pega o nome do usuário de forma segura
        String username = principal.getName(); // MUDANÇA AQUI

        userEmails.put(username, email);
        System.out.println("Email do usuário " + username + " alterado para " + email);
        return "redirect:/";
    }
}