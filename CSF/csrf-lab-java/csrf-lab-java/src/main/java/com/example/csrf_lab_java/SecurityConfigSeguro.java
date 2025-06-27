package com.example.csrf_lab_java;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import static org.springframework.security.config.Customizer.withDefaults;

// @Configuration
@EnableWebSecurity
public class SecurityConfigSeguro {

        @Bean
        public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
                http
                                // PROTEÇÃO CSRF ESTÁ ATIVADA POR PADRÃO! Não precisamos fazer nada.
                                // O código csrf().disable() FOI REMOVIDO.
                                .authorizeHttpRequests(auth -> auth
                                                .requestMatchers("/login").permitAll()
                                                .anyRequest().authenticated())
                                .formLogin(form -> form
                                                .loginPage("/login")
                                                .defaultSuccessUrl("/", true)
                                                .permitAll())
                                .logout(logout -> logout.permitAll());
                return http.build();
        }
}
