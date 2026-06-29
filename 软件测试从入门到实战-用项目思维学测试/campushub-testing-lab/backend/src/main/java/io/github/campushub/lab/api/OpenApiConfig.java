package io.github.campushub.lab.api;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import java.util.List;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI campusHubOpenApi() {
        return new OpenAPI()
            .info(new Info()
                .title("CampusHub Testing Lab API")
                .version("0.2.0-SNAPSHOT")
                .description("""
                    CampusHub 教学项目接口契约。当前接口用于软件测试学习场景，登录 token 为演示值，不代表生产级认证方案。
                    """)
                .license(new License().name("MIT").url("https://opensource.org/license/mit")))
            .servers(List.of(
                new Server().url("http://localhost:8080").description("本地默认后端"),
                new Server().url("http://localhost:18080").description("本地备用端口示例")
            ));
    }
}
