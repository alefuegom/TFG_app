package alefuegom.tfg.model;

import java.time.LocalDate;

import javax.persistence.Entity;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;

@Entity
@Table(name="facturas")
public class Factura extends BaseEntity{
	
	private LocalDate fechaExpedicion;
	
	@NotBlank
	private String emisor;
	
	@NotBlank
	private String receptor;
	
	@NotBlank
	private String descripcion;
	
	private int importe;
	
	private int tipoImpositivo;
	
	private LocalDate fechaOperacion;

	public LocalDate getFechaExpedicion() {
		return fechaExpedicion;
	}

	public void setFechaExpedicion(LocalDate fechaExpedicion) {
		this.fechaExpedicion = fechaExpedicion;
	}

	public String getEmisor() {
		return emisor;
	}

	public void setEmisor(String emisor) {
		this.emisor = emisor;
	}

	public String getReceptor() {
		return receptor;
	}

	public void setReceptor(String receptor) {
		this.receptor = receptor;
	}

	public String getDescripcion() {
		return descripcion;
	}

	public void setDescripcion(String descripcion) {
		this.descripcion = descripcion;
	}

	public int getImporte() {
		return importe;
	}

	public void setImporte(int importe) {
		this.importe = importe;
	}

	public int getTipoImpositivo() {
		return tipoImpositivo;
	}

	public void setTipoImpositivo(int tipoImpositivo) {
		this.tipoImpositivo = tipoImpositivo;
	}

	public LocalDate getFechaOperacion() {
		return fechaOperacion;
	}

	public void setFechaOperacion(LocalDate fechaOperacion) {
		this.fechaOperacion = fechaOperacion;
	}
	
	
	

}
