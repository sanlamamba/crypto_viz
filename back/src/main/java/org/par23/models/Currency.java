package org.par23.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "currencies")
public class Currency {

    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "name")
    private String name;

    @Column(name = "price")
    private Double price;

    @Column(name = "market_cap")
    private Double marketCap;

    @ElementCollection
    @CollectionTable(name = "currency_price_history", joinColumns = @JoinColumn(name = "currency_id"))
    @Column(name = "price_history")
    private List<Double> priceHistory;

    @ElementCollection
    @CollectionTable(name = "currency_market_cap_history", joinColumns = @JoinColumn(name = "currency_id"))
    @Column(name = "market_cap_history")
    private List<Double> marketCapHistory;

    @Column(name = "date")
    private LocalDateTime date = LocalDateTime.now();

}
