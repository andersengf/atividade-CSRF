package com.example.csrf_lab_java;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfigVulneravel {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                // 1. DESABILITA A PROTEÇÃO CSRF PADRÃO DO SPRING SECURITY
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/login").permitAll() // A página de login é pública
                        .anyRequest().authenticated() // Todas as outras páginas exigem login
                )
                .formLogin(form -> form
                        .loginPage("/login") // Define a URL da nossa página de login customizada
                        .defaultSuccessUrl("/", true) // Redireciona para a home após o login
                        .permitAll())
                .logout(logout -> logout.permitAll());

        return http.build();
    }
}