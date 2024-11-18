package org.par23.repositories;

import org.par23.models.Currency;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CurrencyRepository extends JpaRepository<Currency, String> {
    Optional<Currency> findByName(String name);

    Optional<Currency> findBySymbol(String symbol);
}