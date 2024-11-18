package org.par23.repositories;

import org.par23.models.CurrencyData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CurrencyDataRepository extends JpaRepository<CurrencyData, String> {
    Optional<CurrencyData> findByCurrencyId(String currencyId);

    Optional<CurrencyData> findByCurrencyName(String currencyName);
}