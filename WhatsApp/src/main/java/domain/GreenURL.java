package domain;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class GreenURL {

    private final String domain = "https://api.greenapi.com/waInstance";
    private final String instanceId = "7103884803";


}
