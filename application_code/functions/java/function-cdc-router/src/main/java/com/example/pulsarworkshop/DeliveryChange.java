<<<<<<< HEAD
<<<<<<<< HEAD:application_code/functions/java/function-cdc-router/src/main/java/com/example/pulsarworkshop/DeliveryChange.java
package com.example.pulsarworkshop;
========
package com.example.pulsarworkshop.function-astradb-v1;
>>>>>>>> 7b273c6 (Moved function code to new directory structure and resolved some errors. Still not completely working yet.):application_code/functions/java/function-astradb-v1/src/main/java/com/example/pulsarworkshop/function_astradb_writer/DeliveryChange.java
=======
package com.example.pulsarworkshop;
>>>>>>> db504cd (Updated more things to allow Jar to be discoverable)

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;

@Data
@Builder
@NonNull
@AllArgsConstructor
@NoArgsConstructor
public class DeliveryChange {
    private Integer old_customer_id;
    private String old_order_status;
    private String old_delivery_status;
    private String old_customer_lname;
    private String old_customer_city;
    private String old_customer_country;
    private String old_customer_fname;
    private Integer old_order_id;
    private Integer old_category_id;
    private Long old_updated_time;
    private Boolean old_late_delivery_risk;

    private Integer new_customer_id;
    private String new_order_status;
    private String new_delivery_status;
    private String new_customer_lname;
    private String new_customer_city;
    private String new_customer_country;
    private String new_customer_fname;
    private Integer new_order_id;
    private Integer new_category_id;
    private Long new_updated_time;
    private Boolean new_late_delivery_risk;
<<<<<<< HEAD
}
=======
}
>>>>>>> db504cd (Updated more things to allow Jar to be discoverable)
