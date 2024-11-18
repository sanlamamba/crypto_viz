package org.par23.models;

import jakarta.json.bind.annotation.JsonbTransient;
import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "currencies")
public class Currency {

    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "name", nullable = false, unique = true)
    private String name;

    @Column(name = "symbol", nullable = false, unique = true)
    private String symbol;

    @JsonbTransient
    @OneToOne(mappedBy = "currency", cascade = CascadeType.ALL, orphanRemoval = true)
    private CurrencyData currentData;

    @JsonbTransient
    @OneToMany(mappedBy = "currency", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<CurrencyDataHistory> history;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public CurrencyData getCurrentData() {
        return currentData;
    }

    public void setCurrentData(CurrencyData currentData) {
        this.currentData = currentData;
    }

    public List<CurrencyDataHistory> getHistory() {
        return history;
    }

    public void setHistory(List<CurrencyDataHistory> history) {
        this.history = history;
    }
}
