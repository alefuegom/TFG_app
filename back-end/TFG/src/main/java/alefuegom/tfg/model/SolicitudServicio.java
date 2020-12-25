package alefuegom.tfg.model;

import java.time.LocalDateTime;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.sun.istack.NotNull;

@Entity
@Table(name="solicitudServicios")
public class SolicitudServicio extends BaseEntity{
		
	@NotNull
	@Enumerated(EnumType.ORDINAL) 
	private EstadoSolicitud estado;
	
	@NotNull
	private LocalDateTime date;
	
	private String observaciones;
	
	@ManyToOne(cascade= CascadeType.ALL)
	private Tratamiento tratamiento;
	
	@ManyToOne(cascade= CascadeType.ALL)
	private Plaga plaga;
	
	@ManyToOne(optional = true, cascade=CascadeType.ALL)
	private Cliente cliente;
	
	@ManyToOne(optional = true, cascade=CascadeType.ALL)
	private Empresa empresa;
	

	public EstadoSolicitud getEstado() {
		return estado;
	}

	public void setEstado(EstadoSolicitud estado) {
		this.estado = estado;
	}

	public LocalDateTime getDate() {
		return date;
	}

	public void setDate(LocalDateTime date) {
		this.date = date;
	}

	public String getObservaciones() {
		return observaciones;
	}

	public void setObservaciones(String observaciones) {
		this.observaciones = observaciones;
	}

	public Tratamiento getTratamiento() {
		return tratamiento;
	}

	public void setTratamiento(Tratamiento tratamiento) {
		this.tratamiento = tratamiento;
	}

	public Plaga getPlaga() {
		return plaga;
	}

	public void setPlaga(Plaga plaga) {
		this.plaga = plaga;
	}

	public Cliente getCliente() {
		return cliente;
	}

	public void setCliente(Cliente cliente) {
		this.cliente = cliente;
	}

	public Empresa getEmpresa() {
		return empresa;
	}

	public void setEmpresa(Empresa empresa) {
		this.empresa = empresa;
	}
	
	
	
	

}
