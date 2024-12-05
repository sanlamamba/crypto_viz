package org.par23.models;

import jakarta.json.bind.annotation.JsonbTransient;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "currency_data_history")
public class CurrencyDataHistory {

    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "currency_id", nullable = false)
    private String currencyId;

    @Column(name = "price", nullable = false)
    private Double price;

    @Column(name = "market_cap")
    private Double marketCap;

    @Column(name = "source", nullable = true, columnDefinition = "varchar(255) default 'unknown'")
    private String source;

    @Column(name = "trust_factor", nullable = true, columnDefinition = "float default 0.0")
    private Double trustFactor;

    @Column(name = "timestamp", nullable = false)
    private LocalDateTime timestamp = LocalDateTime.now();

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    @JsonbTransient
    @ManyToOne
    @JoinColumn(name = "currency_id", referencedColumnName = "id", insertable = false, updatable = false)
    private Currency currency;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getCurrencyId() {
        return currencyId;
    }

    public void setCurrencyId(String currencyId) {
        this.currencyId = currencyId;
    }

    public Double getPrice() {
        return price;
    }

    public void setPrice(Double price) {
        this.price = price;
    }

    public Double getMarketCap() {
        return marketCap;
    }

    public void setMarketCap(Double marketCap) {
        this.marketCap = marketCap;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public Double getTrustFactor() {
        return trustFactor;
    }

    public void setTrustFactor(Double trustFactor) {
        this.trustFactor = trustFactor;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public Currency getCurrency() {
        return currency;
    }

    public void setCurrency(Currency currency) {
        this.currency = currency;
    }
}